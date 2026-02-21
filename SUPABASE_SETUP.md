# Supabase Setup Guide for KrishiSahay

Complete guide for setting up Supabase database for KrishiSahay.

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click **"New Project"**
4. Fill in:
   - **Project name**: `krishisahay` (or your choice)
   - **Database password**: Choose a strong password (save it!)
   - **Region**: Choose closest to you (e.g., Mumbai for India)
5. Click **"Create new project"**
6. Wait for project to be created (takes 1-2 minutes)

## Step 2: Get Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (for frontend - starts with `eyJ...`)
   - **service_role key** (for backend - keep this secret! Starts with `eyJ...`)

**Important:** 
- **anon key** is safe for frontend (public)
- **service_role key** is for backend only (has admin access)

## Step 3: Run Database Migrations

### Option A: Using Supabase Dashboard (Recommended)

1. Go to **SQL Editor** in Supabase dashboard
2. Click **"New Query"**
3. Open file: `supabase/migrations/20260220020000_create_krishisahay_tables.sql`
4. Copy **all contents** of the file
5. Paste into SQL Editor
6. Click **"Run"** (or press Ctrl+Enter)
7. Verify success message: "Success. No rows returned"
8. Go to **Table Editor** to verify tables are created:
   - `query_cache`
   - `user_feedback`
   - `image_analysis`
   - `app_feedback`

### Option B: Using Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login

# Link your project
supabase link --project-ref your-project-ref

# Run migrations
supabase db push
```

## Step 4: Configure Environment Variables

### Frontend (.env file in project root)

Create or update `.env` file:

```env
# API base URL - use /api in dev (proxied to backend)
VITE_API_URL=/api

# Supabase (for frontend + backend)
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Backend (backend/.env file)

Create `backend/.env` file:

```env
# Supabase (primary database)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# Or use service_role key for admin operations:
# SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# MySQL (fallback when Supabase not configured)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=krishisahay
```

**Important:** 
- Never commit `.env` files with real keys to git!
- Add `.env` to `.gitignore`
- Use environment variables in production

## Step 5: Install Backend Dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

This will install:
- `supabase` (Python client)
- `python-dotenv` (for environment variables)
- Other dependencies

## Step 6: Verify Connection

### Test Backend Connection

```bash
cd backend
python main.py
```

Look for in the output:
```
Database: Using Supabase
```

If you see "Database: Using MySQL" or "Database: No backend", check your `.env` file.

### Test Frontend Connection

1. Start frontend: `npm run dev`
2. Open browser console (F12)
3. Check for any Supabase errors
4. Submit a query and check if it's saved to Supabase

### Manual Test

```bash
cd backend
python -c "from database import Database; db = Database(); print('Connected!' if db.is_connected() else 'Not connected')"
```

## Step 7: Create Storage Bucket (Optional - for Image Storage)

If you want to store uploaded images in Supabase Storage:

1. Go to **Storage** in Supabase dashboard
2. Click **"New bucket"**
3. Name: `agricultural-images`
4. Make it **Public** (or private with RLS policies)
5. Click **"Create bucket"**

Then update `backend/image_analyzer.py` to upload images to this bucket.

## Database Schema

The migration creates these tables:

### 1. query_cache
Stores query-response pairs for caching.

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `query` (TEXT)
- `query_lower` (TEXT) - Lowercase for case-insensitive search
- `language` (TEXT) - Language code
- `answer` (TEXT)
- `category` (TEXT)
- `hit_count` (INTEGER) - Number of times cached
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- Unique on (`query_lower`, `language`)
- Index on `updated_at` DESC

### 2. user_feedback
Stores user feedback on answers.

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `query` (TEXT)
- `answer` (TEXT)
- `feedback` (TEXT) - 'positive' or 'negative'
- `created_at` (TIMESTAMP)

### 3. image_analysis
Stores image analysis results.

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `image_filename` (TEXT)
- `analysis_result` (JSONB) - Full analysis data
- `language` (TEXT)
- `user_query` (TEXT)
- `recommendations` (TEXT)
- `category` (TEXT)
- `created_at` (TIMESTAMP)

### 4. app_feedback
Stores general app feedback with ratings.

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `rating` (SMALLINT) - 1-5 or NULL
- `message` (TEXT)
- `page` (TEXT) - Which page feedback is from
- `created_at` (TIMESTAMP)

## Row Level Security (RLS)

All tables have RLS enabled with public read/write policies for development.

**Current Policies:**
- Public SELECT (read)
- Public INSERT (write)
- Public UPDATE (for query_cache)

**For Production:**
1. Review and tighten RLS policies
2. Consider adding authentication
3. Use service_role key only on backend
4. Use anon key on frontend
5. Add user-based policies

## Troubleshooting

### "Supabase credentials not found"
- Check that `.env` files exist in correct locations
- Verify environment variable names match exactly:
  - `SUPABASE_URL` or `VITE_SUPABASE_URL`
  - `SUPABASE_ANON_KEY` or `VITE_SUPABASE_ANON_KEY`
- Restart backend server after changing `.env`
- Check file encoding (should be UTF-8)

### "Permission denied" errors
- Check RLS policies in Supabase dashboard
- Verify you're using the correct key:
  - `anon` key for frontend
  - `service_role` key for backend (if needed)
- Check table permissions in Supabase

### Connection timeout
- Check your internet connection
- Verify Supabase URL is correct
- Check Supabase project status (dashboard)
- Verify firewall/proxy settings

### "Table does not exist"
- Run the migration again in SQL Editor
- Check migration file syntax
- Verify tables in Table Editor

### Backend falls back to MySQL
- Check `backend/.env` has correct Supabase credentials
- Verify Supabase project is active
- Check backend logs for connection errors

## Production Considerations

### Security

1. **Environment Variables:**
   - Use environment variables, never hardcode keys
   - Use service_role key only on backend
   - Use anon key on frontend
   - Rotate keys periodically

2. **RLS Policies:**
   - Enable Row Level Security
   - Create user-specific policies
   - Limit public access
   - Add authentication

3. **API Keys:**
   - Never expose service_role key
   - Use anon key on frontend only
   - Monitor API usage

### Performance

1. **Indexes:**
   - Already created for frequently queried columns
   - Monitor query performance
   - Add more indexes if needed

2. **Connection Pooling:**
   - Supabase handles this automatically
   - Monitor connection usage
   - Adjust pool size if needed

3. **Caching:**
   - Use query_cache table effectively
   - Monitor cache hit rates
   - Clear old cache entries periodically

### Backup

1. **Automatic Backups:**
   - Enable in Supabase dashboard
   - Set backup schedule
   - Test restore process

2. **Manual Backups:**
   - Export data regularly
   - Keep migration files versioned
   - Document schema changes

3. **Disaster Recovery:**
   - Keep backup of migration files
   - Document recovery procedure
   - Test restore process

## Next Steps

After setup:
1. ✅ Test query caching
2. ✅ Test feedback submission
3. ✅ Test image analysis storage
4. ✅ Monitor Supabase dashboard for data
5. ✅ Review RLS policies for production
6. ✅ Set up automatic backups
7. ✅ Monitor API usage

## Verification Checklist

- [ ] Supabase project created
- [ ] Migration ran successfully
- [ ] All 4 tables exist
- [ ] Environment variables configured
- [ ] Backend connects to Supabase
- [ ] Frontend connects to Supabase
- [ ] Query caching works
- [ ] Feedback submission works
- [ ] Image analysis storage works
- [ ] RLS policies reviewed

## Support

For Supabase-specific issues:
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- [Supabase GitHub](https://github.com/supabase/supabase)

For KrishiSahay issues:
- Check backend logs
- Check browser console
- Review this guide
- See main README.md
