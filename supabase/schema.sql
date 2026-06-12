-- Mission Ready Vacations AI Supabase-ready schema
-- All provider prices must be treated as estimates until confirmed by travel providers.
create extension if not exists "pgcrypto";

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  full_name text,
  role text not null default 'user',
  created_at timestamptz not null default now()
);

create table if not exists public.family_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  home_city_or_duty_station text,
  nearest_airport text,
  family_size int,
  kids_ages text,
  pets text,
  preferred_hotel_type text,
  driving_limit text,
  monthly_travel_budget numeric,
  need_kitchen_laundry boolean default false,
  need_refundable_bookings boolean default true,
  military_discount_preference boolean default false,
  created_at timestamptz not null default now()
);

create table if not exists public.trip_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  mode text not null check (mode in ('family','leave')),
  departure_city text,
  destination text,
  travel_dates text,
  budget numeric,
  family_size int,
  structured_answers jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.trip_results (
  id uuid primary key default gen_random_uuid(),
  trip_request_id uuid references public.trip_requests(id) on delete cascade,
  option_type text not null,
  mission_ready_score int not null check (mission_ready_score between 1 and 100),
  estimated_real_trip_cost numeric not null,
  cost_breakdown jsonb not null,
  itinerary jsonb not null default '[]'::jsonb,
  hidden_cost_warnings jsonb not null default '[]'::jsonb,
  family_stress_warnings jsonb not null default '[]'::jsonb,
  rationale text,
  provider_link_placeholder text,
  created_at timestamptz not null default now()
);

create table if not exists public.saved_trips (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  trip_result_id uuid references public.trip_results(id) on delete cascade,
  label text,
  created_at timestamptz not null default now()
);

create table if not exists public.payments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  provider text not null check (provider in ('stripe','paypal')),
  plan text not null,
  amount numeric not null,
  currency text not null default 'usd',
  status text not null default 'placeholder_pending',
  hosted_checkout_url text,
  provider_session_id text,
  created_at timestamptz not null default now()
);

create table if not exists public.affiliate_clicks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  trip_result_id uuid references public.trip_results(id) on delete set null,
  provider text,
  destination_url text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.concierge_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  name text not null,
  email text not null,
  phone text,
  trip_destination text,
  travel_dates text,
  budget numeric,
  family_size int,
  military_family boolean default false,
  main_concern text,
  notes text,
  status text not null default 'new',
  created_at timestamptz not null default now()
);

create table if not exists public.destination_packages (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  description text,
  options jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.admin_notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  related_table text,
  related_id uuid,
  note text not null,
  created_at timestamptz not null default now()
);
