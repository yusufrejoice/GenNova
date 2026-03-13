-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Text Generation History Table (Rebuilt)
CREATE TABLE IF NOT EXISTS text_generations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    tool_type TEXT NOT NULL,           -- 'product_description', 'blog', 'caption', etc.
    input_data JSONB NOT NULL,
    generated_text TEXT NOT NULL,
    model_id TEXT NOT NULL,
    action_type TEXT NOT NULL DEFAULT 'generate', -- 'generate', 'regenerate', 'refine', 'edit'
    parent_id UUID REFERENCES text_generations(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE text_generations ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only view their own generations
DROP POLICY IF EXISTS "Users can view their own generations" ON text_generations;
CREATE POLICY "Users can view their own generations" 
ON text_generations FOR SELECT 
USING (auth.uid() = user_id);

-- Policy: Allow service-side insertion (essential for backend-triggered saves)
DROP POLICY IF EXISTS "Allow service-side insertion" ON text_generations;
CREATE POLICY "Allow service-side insertion" 
ON text_generations FOR INSERT 
WITH CHECK (true);

-- Policy: Users can update their own generations (for manual edits)
DROP POLICY IF EXISTS "Users can update their own generations" ON text_generations;
CREATE POLICY "Users can update their own generations" 
ON text_generations FOR UPDATE
USING (auth.uid() = user_id);

-- Image Generations Table
CREATE TABLE IF NOT EXISTS image_generations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    model_id TEXT NOT NULL,
    image_url TEXT,
    bucket_path TEXT,
    status TEXT DEFAULT 'success',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE image_generations ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view their own images" ON image_generations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Allow service-side image insertion" ON image_generations
    FOR INSERT WITH CHECK (true);
