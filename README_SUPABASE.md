# Supabase Integration - Quick Reference

## ✅ What's Been Updated

1. **Backend Database** - Now uses Supabase (primary) with MySQL fallback
2. **All Data Storage** - Query cache, feedback, and image analysis stored in Supabase
3. **Environment Variables** - Configured for both frontend and backend
4. **Automatic Fallback** - Falls back to MySQL or no-database mode if Supabase unavailable

## 🚀 Quick Setup

### 1. Get Supabase Credentials

1. Go to [supabase.com](https://supabase.com) and create a project
2. Go to **Settings** → **API**
3. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (for frontend)
   - **service_role key** (for backend - optional, use anon key works too)

### 2. Run Database Migration

In Supabase Dashboard → **SQL Editor**:
- Copy contents of `supabase/migrations/20260220020000_create_krishisahay_tables.sql`
- Paste and click **Run**
- Verify tables created in **Table Editor**

### 3. Configure Environment Variables

**Frontend** (`.env` in project root):
```env
VITE_API_URL=/api
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Backend** (`backend/.env`):
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# Or: SUPABASE_SERVICE_ROLE_KEY=eyJ... (for admin ops)
```

### 4. Install Dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

### 5. Restart Backend

```bash
cd backend
python main.py
```

Look for: `Database: Using Supabase` in the output.

## 📊 Database Tables

All data is now stored in Supabase:

- **query_cache** - Cached query responses (with hit_count tracking)
- **user_feedback** - User feedback on answers (positive/negative)
- **image_analysis** - Image analysis results (with JSONB analysis data)
- **app_feedback** - General app feedback with ratings (1-5 stars)

## 🔍 Verify Connection

Check backend logs for:
```
Database: Using Supabase
```

If you see warnings or "Using MySQL", check your `.env` files.

### Test Query

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "How to grow rice?", "language": "en"}'
```

Then check Supabase Table Editor → `query_cache` table - you should see the cached response.

## 🔄 Fallback Behavior

The system automatically falls back:

1. **Supabase** (primary) - if credentials configured
2. **MySQL** (fallback) - if Supabase unavailable but MySQL configured
3. **No database** (fallback) - if neither configured (caching disabled)

This ensures the app always works, even without database setup.

## 📝 Full Documentation

See `SUPABASE_SETUP.md` for:
- Detailed setup instructions
- Database schema explanation
- RLS policy configuration
- Production considerations
- Troubleshooting guide

## 🎯 Quick Commands

```bash
# Test Supabase connection
cd backend
python -c "from database import Database; db = Database(); print('Supabase' if db.is_connected() else 'Not connected')"

# View tables in Supabase
# Go to: Supabase Dashboard → Table Editor

# Check RLS policies
# Go to: Supabase Dashboard → Authentication → Policies
```

## ⚠️ Important Notes

- **Never commit `.env` files** with real keys to git
- **Use anon key** on frontend (safe for public)
- **Use service_role key** only on backend (has admin access)
- **RLS is enabled** - review policies for production
- **Backups** - enable automatic backups in Supabase dashboard

## 🚀 Production Checklist

- [ ] Supabase project created
- [ ] Migration ran successfully
- [ ] Environment variables configured
- [ ] RLS policies reviewed
- [ ] Automatic backups enabled
- [ ] API usage monitored
- [ ] Connection tested
- [ ] Data verified in dashboard
