-- مساعد الطبيب: rosters readable only with the shared doctors' code, writable only by admins.
create extension if not exists pgcrypto with schema extensions;

create table if not exists public.duty (
  id bigint generated always as identity primary key,
  dept text not null,
  day date not null,
  level text not null default 'oth' check (level in ('res', 'spec', 'cons', 'oth')),
  name text not null,
  phone text not null default '',
  start_t text not null default '',
  end_t text not null default '',
  note text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists duty_day on public.duty (day);

create table if not exists public.admins (
  user_id uuid primary key references auth.users on delete cascade
);

create table if not exists public.settings (
  id int primary key default 1 check (id = 1),
  code_hash text not null,
  updated_at timestamptz not null default now()
);

alter table public.duty enable row level security;
alter table public.admins enable row level security;
alter table public.settings enable row level security;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where user_id = auth.uid())
$$;

drop policy if exists duty_admin on public.duty;
create policy duty_admin on public.duty for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

drop policy if exists admins_self on public.admins;
create policy admins_self on public.admins for select to authenticated
  using (user_id = auth.uid());

-- Doctors: the roster for a date range, only with the right code. bcrypt cost 10 slows guessing.
create or replace function public.get_duty(p_code text, p_from date, p_to date)
returns setof public.duty
language plpgsql stable security definer set search_path = public, extensions as $$
begin
  if p_to < p_from or p_to - p_from > 7 then
    raise exception 'range' using errcode = '22023';
  end if;
  if not exists (select 1 from public.settings where code_hash = crypt(coalesce(p_code, ''), code_hash)) then
    raise exception 'bad code' using errcode = '28000';
  end if;
  return query select * from public.duty where day between p_from and p_to order by dept, level, name;
end $$;

create or replace function public.set_access_code(p_code text) returns timestamptz
language plpgsql security definer set search_path = public, extensions as $$
declare t timestamptz;
begin
  if not public.is_admin() then raise exception 'not admin' using errcode = '42501'; end if;
  if length(coalesce(p_code, '')) < 6 then raise exception 'short' using errcode = '22023'; end if;
  insert into public.settings (id, code_hash) values (1, crypt(p_code, gen_salt('bf', 10)))
    on conflict (id) do update set code_hash = excluded.code_hash, updated_at = now()
    returning updated_at into t;
  return t;
end $$;

create or replace function public.code_updated_at() returns timestamptz
language sql stable security definer set search_path = public as $$
  select case when public.is_admin() then (select updated_at from public.settings where id = 1) end
$$;

revoke all on function public.get_duty(text, date, date) from public;
revoke all on function public.set_access_code(text) from public, anon;
revoke all on function public.code_updated_at() from public, anon;
revoke all on function public.is_admin() from public, anon;
grant execute on function public.get_duty(text, date, date) to anon, authenticated;
grant execute on function public.set_access_code(text) to authenticated;
grant execute on function public.code_updated_at() to authenticated;
grant execute on function public.is_admin() to authenticated;
