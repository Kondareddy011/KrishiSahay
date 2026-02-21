# Verify Supabase Connection

## ✅ Configuration Complete

Your Supabase credentials should be configured in:

**Frontend** (`.env` in project root):
- ✅ VITE_SUPABASE_URL configured
- ✅ VITE_SUPABASE_ANON_KEY configured
- ✅ VITE_API_URL configured (should be `/api` for dev)

**Backend** (`backend/.env`):
- ✅ SUPABASE_URL configured
- ✅ SUPABASE_ANON_KEY configured (or SUPABASE_SERVICE_ROLE_KEY)

## 🔍 Next Steps

### 1. Run Database Migration

Before the app can store data, you need to create the tables in Supabase:

1. Go to your Supabase Dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy and paste the contents of `supabase/migrations/20260220020000_create_krishisahay_tables.sql`
5. Click **Run**

This will create:
- `query_cache` table - Cached query responses
- `user_feedback` table - User feedback on answers
- `image_analysis` table - Image analysis results
- `app_feedback` table - General app feedback with ratings

### 2. Restart Backend Server

After creating the tables, restart your backend:

```bash
cd backend
python main.py
```

You should see:
```
Database: Using Supabase
```

If you see "Database: Using MySQL" or "Database: No backend", check your `.env` file.

### 3. Test the Connection

1. Start both servers (backend and frontend)
2. Go to http://localhost:5173 (or port shown)
3. Ask a question or upload an image
4. Check Supabase Dashboard → **Table Editor** to see data being stored

### 4. Verify Data Storage

After using the app:

1. Go to Supabase Dashboard
2. Navigate to **Table Editor**
3. You should see data in:
   - `query_cache` - Cached queries with hit_count
   - `user_feedback` - User feedback (positive/negative)
   - `image_analysis` - Image analysis results (JSONB)
   - `app_feedback` - App feedback with ratings

## 🐛 Troubleshooting

### If you see "Database: Using MySQL" or "Database: No backend":
- Check that `backend/.env` exists
- Verify the file has correct Supabase credentials:
  - `SUPABASE_URL=https://your-project.supabase.co`
  - `SUPABASE_ANON_KEY=eyJ...` (or `SUPABASE_SERVICE_ROLE_KEY`)
- Restart the backend server after changing `.env`

### If you see "relation does not exist":
- Run the database migration SQL script in Supabase SQL Editor
- Check that all 4 tables exist in Supabase Dashboard → Table Editor
- Verify migration ran successfully (should see "Success" message)

### If connection fails:
- Verify your Supabase project is active (check dashboard)
- Check that the URL and key are correct (no extra spaces)
- Ensure RLS policies allow access (they should be public by default)
- Check backend logs for specific error messages

### If backend falls back to MySQL:
- Supabase credentials not found or incorrect
- Check `.env` file location (`backend/.env`)
- Verify environment variable names match exactly
- Restart backend after changing `.env`

## 📊 Check Connection Status

### Backend Logs

When backend starts, look for:
```
Database: Using Supabase
```

### Health Endpoint

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "database_connected": true,
  ...
}
```

### Manual Test

```bash
cd backend
python -c "from database import Database; db = Database(); print('Supabase connected!' if db.is_connected() else 'Not connected')"
```

## ✅ Verification Checklist

- [ ] Supabase project created
- [ ] Migration SQL executed successfully
- [ ] All 4 tables exist in Table Editor
- [ ] `.env` files configured correctly
- [ ] Backend shows "Database: Using Supabase"
- [ ] Can submit queries and see data in Supabase
- [ ] Can submit feedback and see data in Supabase
- [ ] Can upload images and see analysis in Supabase

## 🔄 Fallback Behavior

The system automatically falls back if Supabase is unavailable:

1. **Supabase** (primary) - if credentials configured ✅
2. **MySQL** (fallback) - if Supabase unavailable but MySQL configured
3. **No database** (fallback) - if neither configured (caching disabled)

This ensures the app always works, even without database setup.

## 📝 Next Steps

After verification:
1. ✅ Test query caching (ask same question twice)
2. ✅ Test feedback submission
3. ✅ Test image analysis storage
4. ✅ Monitor Supabase dashboard for data
5. ✅ Review RLS policies for production use

## 🔗 Related Documentation

- Full setup: `SUPABASE_SETUP.md`
- Quick reference: `README_SUPABASE.md`
- Main README: `README.md`
