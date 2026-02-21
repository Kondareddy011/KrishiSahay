-- Create tables for KrishiSahay application

-- Query Cache Table
CREATE TABLE IF NOT EXISTS query_cache (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    query_lower TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'en',
    answer TEXT NOT NULL,
    category TEXT,
    hit_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(query_lower, language)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_query_cache_query_lang ON query_cache(query_lower, language);
CREATE INDEX IF NOT EXISTS idx_query_cache_updated_at ON query_cache(updated_at DESC);

-- User Feedback Table
CREATE TABLE IF NOT EXISTS user_feedback (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    feedback TEXT NOT NULL CHECK (feedback IN ('positive', 'negative')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for feedback queries
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON user_feedback(created_at DESC);

-- Image Analysis Table (for storing image analysis results)
CREATE TABLE IF NOT EXISTS image_analysis (
    id BIGSERIAL PRIMARY KEY,
    image_url TEXT,
    image_filename TEXT,
    analysis_result JSONB NOT NULL,
    language TEXT NOT NULL DEFAULT 'en',
    user_query TEXT,
    recommendations TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for image analysis queries
CREATE INDEX IF NOT EXISTS idx_image_analysis_created_at ON image_analysis(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_image_analysis_category ON image_analysis(category);

-- App Feedback Table
CREATE TABLE IF NOT EXISTS app_feedback (
    id BIGSERIAL PRIMARY KEY,
    rating SMALLINT CHECK (rating >= 1 AND rating <= 5),
    message TEXT NOT NULL,
    page TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_app_feedback_created_at ON app_feedback(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE query_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE image_analysis ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust based on your security needs)
CREATE POLICY "Allow public read access to query_cache" ON query_cache
    FOR SELECT USING (true);

CREATE POLICY "Allow public insert access to query_cache" ON query_cache
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public update access to query_cache" ON query_cache
    FOR UPDATE USING (true);

CREATE POLICY "Allow public insert access to user_feedback" ON user_feedback
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access to user_feedback" ON user_feedback
    FOR SELECT USING (true);

CREATE POLICY "Allow public insert access to image_analysis" ON image_analysis
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access to image_analysis" ON image_analysis
    FOR SELECT USING (true);

ALTER TABLE app_feedback ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public insert access to app_feedback" ON app_feedback FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read access to app_feedback" ON app_feedback FOR SELECT USING (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at
CREATE TRIGGER update_query_cache_updated_at BEFORE UPDATE ON query_cache
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
