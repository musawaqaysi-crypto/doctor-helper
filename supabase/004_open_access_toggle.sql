-- Let admins switch sign-in on/off from the panel instead of running SQL.
create or replace function public.get_open_access() returns boolean
language sql stable security definer set search_path = public as $$
  select case when public.is_admin() then (select open_access from public.app_flags where id = 1) end
$$;
create or replace function public.set_open_access(p_open boolean) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not admin' using errcode = '42501'; end if;
  update public.app_flags set open_access = p_open where id = 1;
  return p_open;
end $$;
revoke all on function public.get_open_access() from public, anon;
revoke all on function public.set_open_access(boolean) from public, anon;
grant execute on function public.get_open_access() to authenticated;
grant execute on function public.set_open_access(boolean) to authenticated;
