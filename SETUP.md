# Setup Instructions - KrishiSahay

Complete step-by-step setup guide for KrishiSahay agricultural AI assistant.

## Step 1: Install Prerequisites

### Python Setup
1. Download Python 3.7+ from [python.org](https://www.python.org/downloads/)
   - **Recommended**: Python 3.8+ for full ML features
2. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### Node.js Setup
1. Download Node.js 18+ from [nodejs.org](https://nodejs.org/)
2. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Ollama Setup (Optional - for Offline AI)
1. Download from [ollama.ai](https://ollama.ai)
2. Install and verify:
   ```bash
   ollama --version
   ollama run llama3.2
   ```

## Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# This will install:
# - fastapi, uvicorn
# - sentence-transformers (for embeddings)
# - faiss-cpu (for vector search, optional)
# - transformers, torch (for ML models, optional)
# - supabase (for database)
# - pymysql (MySQL fallback)
# - Pillow (image processing)
# - python-dotenv
```

**Note:** Installing ML libraries may take a few minutes as they download models and compile code.

### Backend Configuration

Create `backend/.env` file (copy from `backend/.env.example`):

```env
# Supabase (primary database)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key

# MySQL (fallback - optional)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=krishisahay

# Offline AI (Ollama - optional)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Note:** Backend works without Supabase/MySQL/Ollama - it will use mock responses.

## Step 3: Supabase Setup (Optional but Recommended)

### Option A: Using Supabase Dashboard

1. Go to [supabase.com](https://supabase.com) and create a project
2. Go to **SQL Editor** → **New Query**
3. Copy contents of `supabase/migrations/20260220020000_create_krishisahay_tables.sql`
4. Paste and click **Run**
5. Verify tables created in **Table Editor**

### Option B: Skip Supabase

The backend will fall back to MySQL or work without database (caching disabled).

See `SUPABASE_SETUP.md` for detailed instructions.

## Step 4: Build FAISS Index (Optional)

```bash
# Still in backend directory with venv activated
python setup_faiss.py
```

This will:
- Load the agricultural knowledge base
- Generate embeddings using SentenceTransformer
- Create FAISS vector index
- Save index to `backend/faiss_index/agricultural_index.faiss`

**Note:** Not required - system works with Ollama/mock fallback.

## Step 5: Start Backend Server

```bash
# Still in backend directory
python main.py
```

**Expected output:**
```
Initializing KrishiSahay backend...
Database: Using Supabase (or MySQL/No backend)
Ollama (offline AI) available (or not running)
Backend ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open. The backend is now running on `http://localhost:8000`

## Step 6: Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to project root
cd <project-root>

# Install Node.js dependencies
npm install

# This will install:
# - react, react-dom
# - vite
# - tailwindcss
# - typescript
# - @supabase/supabase-js
# - lucide-react
# - and other dependencies
```

## Step 7: Configure Frontend

Create `.env` file in project root:

```bash
# Windows (PowerShell):
echo "VITE_API_URL=/api" > .env
echo "VITE_SUPABASE_URL=https://your-project.supabase.co" >> .env
echo "VITE_SUPABASE_ANON_KEY=your-anon-key" >> .env

# macOS/Linux:
cat > .env << EOF
VITE_API_URL=/api
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
EOF
```

**Note:** `VITE_API_URL=/api` uses Vite proxy in dev (forwards to localhost:8000).

## Step 8: Start Frontend Server

```bash
# In project root directory
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 9: Access Application

1. Open browser
2. Navigate to `http://localhost:5173` (or port shown in terminal)
3. You should see the KrishiSahay homepage

## Step 10: Test the Application

1. Click "Ask AI" in navigation
2. Type a question: "How to grow rice?"
3. Select language: English (or any Indian language)
4. Click "Get Answer"
5. You should receive an AI-generated answer

### Test Mixed Language

Try: "rice pests ela control cheyam" (Telugu + English)

### Test Image Analysis

1. Click "Image Analysis" mode
2. Upload a crop/pest image
3. Get ML-powered analysis

## Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Can access homepage
- [ ] Can submit questions and get answers
- [ ] Language selector works
- [ ] Mixed language queries work
- [ ] Image upload works (if ML models installed)
- [ ] Offline cache working (test by disconnecting internet)
- [ ] Supabase connected (check backend logs)

## Common Issues

### Issue: "FAISS index not found"
**Solution:** Not required - system uses Ollama/mock fallback. To build: `python setup_faiss.py`

### Issue: "Module not found" errors
**Solution:** 
```bash
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** 
1. Find process using port 8000:
   ```bash
   # Windows:
   netstat -ano | findstr :8000
   # macOS/Linux:
   lsof -i :8000
   ```
2. Kill the process or change port in `backend/main.py`

### Issue: "Ollama not available"
**Solution:** 
- Install from https://ollama.ai
- Run: `ollama run llama3.2`
- Or skip - system uses RAG/mock fallback

### Issue: "Supabase connection failed"
**Solution:**
- Check `.env` files have correct credentials
- Verify migration ran successfully
- System falls back to MySQL or no-database mode

### Issue: "CORS error" in browser
**Solution:** Backend CORS is configured to allow all origins. If issues persist, check `backend/main.py` CORS settings.

### Issue: "Cannot connect to API"
**Solution:**
1. Verify backend is running
2. Check `VITE_API_URL` in `.env` file (use `/api` for dev)
3. Test backend directly: `curl http://localhost:8000/health`

### Issue: "Python version too old"
**Solution:** 
- Upgrade to Python 3.8+ for full ML features
- Or use `model_simple.py` and `query_simple.py` in ml-model-repo (works with Python 3.7)

## Next Steps

- Add more agricultural knowledge to `backend/data/agricultural_knowledge.json`
- Customize UI colors and styling
- Deploy to production (see README.md)
- Add more languages
- Fine-tune Ollama models
- Expand ML model repository

## Development Tips

1. **Backend logs:** Check terminal where `python main.py` is running
2. **Frontend logs:** Check browser console (F12)
3. **Database:** Supabase dashboard or MySQL
4. **Cache:** Responses cached in Supabase/MySQL and localStorage
5. **Hot reload:** Both frontend (Vite) and backend (uvicorn) support hot reload
6. **Ollama:** Keep Ollama running for offline AI responses

## Production Deployment

See `README.md` for production deployment instructions.

## ML Model Repository

For advanced ML features, see `ml-model-repo/README.md`:
- Separate repository for ML models
- FAISS + RAG pipeline
- Can be integrated with main backend
