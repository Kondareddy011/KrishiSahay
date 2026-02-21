/*
  # KrishiSahay Database Schema

  ## Overview
  Creates tables for agricultural knowledge base, query caching, and user feedback.

  ## New Tables
  
  ### `agricultural_knowledge`
  - `id` (uuid, primary key) - Unique identifier
  - `category` (text) - Type: crops, pests, fertilizers, schemes, weather
  - `title` (text) - Knowledge article title
  - `content` (text) - Detailed information
  - `keywords` (text[]) - Searchable keywords
  - `language` (text) - Content language (en, te, hi)
  - `created_at` (timestamptz) - Creation timestamp
  
  ### `query_cache`
  - `id` (uuid, primary key) - Unique identifier
  - `query` (text) - User query text
  - `query_lower` (text) - Lowercase for matching
  - `language` (text) - Query language
  - `answer` (text) - Generated response
  - `category` (text) - Detected category
  - `hit_count` (integer) - Cache hit counter
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last access timestamp
  
  ### `user_feedback`
  - `id` (uuid, primary key) - Unique identifier
  - `query` (text) - Original query
  - `answer` (text) - Given answer
  - `feedback` (text) - positive or negative
  - `created_at` (timestamptz) - Feedback timestamp
  
  ## Security
  - RLS enabled on all tables
  - Public read access for knowledge base
  - Public insert for cache and feedback
*/

CREATE TABLE IF NOT EXISTS agricultural_knowledge (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  category text NOT NULL,
  title text NOT NULL,
  content text NOT NULL,
  keywords text[] DEFAULT '{}',
  language text DEFAULT 'en',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS query_cache (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  query text NOT NULL,
  query_lower text NOT NULL,
  language text DEFAULT 'en',
  answer text NOT NULL,
  category text,
  hit_count integer DEFAULT 1,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_feedback (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  query text NOT NULL,
  answer text NOT NULL,
  feedback text NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE agricultural_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE query_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read agricultural knowledge"
  ON agricultural_knowledge FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can read query cache"
  ON query_cache FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can insert into query cache"
  ON query_cache FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Anyone can update query cache"
  ON query_cache FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can insert feedback"
  ON user_feedback FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_knowledge_category ON agricultural_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_language ON agricultural_knowledge(language);
CREATE INDEX IF NOT EXISTS idx_cache_query_lower ON query_cache(query_lower);
CREATE INDEX IF NOT EXISTS idx_cache_language ON query_cache(language);