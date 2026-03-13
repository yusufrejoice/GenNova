# GenNova Authentication System

Production-ready authentication system built with FastAPI, Supabase, and SMTP.

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** Supabase (PostgreSQL)
- **Authentication:** Supabase Auth
- **Email Service:** SMTP (Gmail)

## Project Structure
```text
GenNova/
\u251c\u2500\u2500 app/
\u2502 \u251c\u2500\u2500 core/
\u2502 \u2502 \u251c\u2500\u2500 config.py
\u2502 \u2502 \u2514\u2500\u2500 email_service.py
\u2502 \u251c\u2500\u2500 database/
\u2502 \u2502 \u2514\u2500\u2500 supabase_client.py
\u2502 \u251c\u2500\u2500 modules/
\u2502 \u2502 \u2514\u2500\u2500 auth/
\u2502 \u2502 \u251c\u2500\u2500 auth_routes.py
\u2502 \u2502 \u251c\u2500\u2500 auth_schema.py
\u2502 \u2502 \u251c\u2500\u2500 auth_service.py
\u2502 \u2502 \u2514\u2500\u2500 auth_dependencies.py
\u2502 \u2514\u2500\u2500 main.py
\u251c\u2500\u2500 .env
\u251c\u2500\u2500 requirements.txt
\u2514\u2500\u2500 README.md
```

## Setup Instructions

### 1. Supabase Database Setup
Run the following SQL in your Supabase SQL Editor to create the `profiles` table:

```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  name text,
  email text unique,
  role text default 'user',
  created_at timestamptz default now()
);

-- Enable row level security
alter table public.profiles enable row level security;

-- Create policies (Example: users can read their own profiles)
create policy "Users can view own profile" 
on public.profiles for select 
using (auth.uid() = id);

create policy "Users can update own profile" 
on public.profiles for update 
using (auth.uid() = id);

-- Allow service role to insert profiles (needed for our backend)
create policy "Backend can insert profiles"
on public.profiles for insert
with check (true);
```

### 2. Environment Variables
Ensure your `.env` file is populated:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password
```

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

## API Endpoints
- **POST /auth/signup**: Register a new user
- **POST /auth/login**: Login and receive JWT
- **GET /auth/me**: Get current user profile (requires Bearer Token)
