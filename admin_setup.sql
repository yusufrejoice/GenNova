-- 1. Update Profiles table with Credits and Ban timestamp
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS credits INTEGER DEFAULT 10,
ADD COLUMN IF NOT EXISTS banned_until TIMESTAMPTZ DEFAULT NULL;

-- 2. Create App Models table for global model status control
CREATE TABLE IF NOT EXISTS public.app_models (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'image', 'text', etc.
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Insert existing models into app_models (Example models)
INSERT INTO public.app_models (id, name, type) VALUES
('wavespeed-ai/flux-dev-lora-ultra-fast', 'Flux Ultra Fast', 'image'),
('meta-llama/Llama-3.1-8B-Instruct', 'Llama 3.1 8B', 'text'),
('Qwen/Qwen2.5-7B-Instruct', 'Qwen 2.5 7B', 'text')
ON CONFLICT (id) DO NOTHING;

-- 4. RLS for app_models (Public read, Admin write)
ALTER TABLE public.app_models ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read on app_models"
ON public.app_models FOR SELECT
USING (true);

-- Note: Profile role-based policies should already exist or be managed by service role
