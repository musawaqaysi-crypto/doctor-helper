-- Doctors sign in with their employee number + last 4 digits of their mobile, instead of one shared code.
create table if not exists public.staff (
  emp_id text primary key,
  name text not null default '',
  pin text not null check (pin ~ '^\d{4}$'),
  active boolean not null default true,
  last_seen timestamptz,
  created_at timestamptz not null default now()
);
alter table public.staff enable row level security;
drop policy if exists staff_admin on public.staff;
create policy staff_admin on public.staff for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

create table if not exists public.login_fails (
  emp_id text not null,
  at timestamptz not null default now()
);
create index if not exists login_fails_emp on public.login_fails (emp_id, at);
alter table public.login_fails enable row level security;

drop function if exists public.get_duty(text, date, date);
drop function if exists public.set_access_code(text);
drop function if exists public.code_updated_at();
drop table if exists public.settings;

-- Returns {ok, name, rows} or {ok:false, reason}; failures are recorded (not raised) so the 5-per-15-min limit sticks.
create or replace function public.get_duty(p_emp text, p_pin text, p_from date, p_to date)
returns json
language plpgsql volatile security definer set search_path = public as $$
declare s public.staff; fails int;
begin
  if p_to < p_from or p_to - p_from > 7 then
    return json_build_object('ok', false, 'reason', 'range');
  end if;
  select count(*) into fails from public.login_fails
    where emp_id = coalesce(p_emp, '') and at > now() - interval '15 minutes';
  if fails >= 5 then
    return json_build_object('ok', false, 'reason', 'locked');
  end if;
  select * into s from public.staff where emp_id = p_emp;
  if not found or s.pin <> coalesce(p_pin, '') then
    insert into public.login_fails (emp_id) values (coalesce(p_emp, ''));
    return json_build_object('ok', false, 'reason', 'bad');
  end if;
  if not s.active then
    return json_build_object('ok', false, 'reason', 'inactive');
  end if;
  update public.staff set last_seen = now() where emp_id = p_emp;
  delete from public.login_fails where at < now() - interval '1 day';
  return json_build_object('ok', true, 'name', s.name, 'rows',
    coalesce((select json_agg(d order by d.dept, d.level, d.name) from public.duty d where d.day between p_from and p_to), '[]'::json));
end $$;

revoke all on function public.get_duty(text, text, date, date) from public;
grant execute on function public.get_duty(text, text, date, date) to anon, authenticated;
