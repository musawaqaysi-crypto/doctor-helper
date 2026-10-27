-- Temporary switch: while open_access is true the roster is readable without signing in.
create table if not exists public.app_flags (
  id int primary key default 1 check (id = 1),
  open_access boolean not null default false
);
alter table public.app_flags enable row level security;
insert into public.app_flags (id, open_access) values (1, true)
  on conflict (id) do update set open_access = excluded.open_access;

create or replace function public.get_duty(p_emp text, p_pin text, p_from date, p_to date)
returns json
language plpgsql volatile security definer set search_path = public as $$
declare s public.staff; fails int;
begin
  if p_to < p_from or p_to - p_from > 7 then
    return json_build_object('ok', false, 'reason', 'range');
  end if;
  if (select open_access from public.app_flags where id = 1) then
    return json_build_object('ok', true, 'name', coalesce((select name from public.staff where emp_id = p_emp and pin = p_pin and active), ''), 'rows',
      coalesce((select json_agg(d order by d.dept, d.level, d.name) from public.duty d where d.day between p_from and p_to), '[]'::json));
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
