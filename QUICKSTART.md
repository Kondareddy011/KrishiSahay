# Quick Start Guide - KrishiSahay

## 🚀 Fast Setup (5 minutes)

### Prerequisites Check
```bash
python --version  # Should be 3.7+ (3.8+ recommended)
node --version    # Should be 18+
npm --version
```

### Step 1: Backend (Terminal 1)

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Optional: Configure Supabase (or skip - uses fallback)
# Copy backend/.env.example to backend/.env and add credentials

python main.py
```

✅ Backend running on `http://localhost:8000`

**Optional: Setup Ollama for Offline AI**
```bash
# Install from https://ollama.ai
ollama run llama3.2
```

### Step 2: Frontend (Terminal 2)

```bash
# In project root
npm install

# Optional: Configure Supabase
# Copy .env.example to .env and add credentials

npm run dev
```

✅ Frontend running on `http://localhost:5173` (or next available port)

### Step 3: Test

1. Open `http://localhost:5173` in browser
2. Click "Ask AI" in navigation
3. Type: "How to grow rice?"
4. Select language: English (or any Indian language)
5. Click "Get Answer"

## 🧪 Test Features

### Test Mixed Language
Try: "rice pests ela control cheyam" (Telugu + English)

### Test Image Analysis
1. Click "Image Analysis" mode
2. Upload a crop image
3. Get ML-powered analysis

### Test Voice Input
1. Click microphone icon
2. Speak your question
3. Get transcribed text

## 📁 Important Files

- `backend/main.py` - FastAPI server
- `backend/model.py` - RAG pipeline
- `backend/ollama_client.py` - Offline AI client
- `backend/database.py` - Supabase/MySQL manager
- `src/pages/AskAIPage.tsx` - Main AI interface
- `src/services/api.ts` - API client
- `.env` - Frontend environment variables
- `backend/.env` - Backend environment variables

## ⚠️ Troubleshooting

**Backend won't start:**
- Check Python version: `python --version`
- Activate venv: `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`

**Ollama not working:**
- Install from https://ollama.ai
- Run: `ollama run llama3.2`
- Or skip - system uses RAG/mock fallback

**Frontend can't connect:**
- Check backend is running on port 8000
- Verify `.env` file has `VITE_API_URL=/api`
- Check browser console (F12) for errors

**Port already in use:**
- Change port in `backend/main.py` (line ~400)
- Or kill process using port 8000/5173

**Supabase errors:**
- Check `.env` files have correct credentials
- Or skip Supabase - system uses MySQL/no-database fallback

## 📚 Full Documentation

- `README.md` - Complete project documentation
- `SETUP.md` - Detailed setup instructions
- `SUPABASE_SETUP.md` - Supabase configuration guide
- `ml-model-repo/README.md` - ML model repository guide

## 🎯 Quick Commands

```bash
# Start backend
cd backend && python main.py

# Start frontend
npm run dev

# Test backend API
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "How to grow rice?", "language": "en"}'
```

## 🌍 Supported Languages

All major Indian languages:
- English, Hindi, Telugu, Tamil, Bengali, Marathi, Gujarati
- Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu
- **Mixed** - Any Indian language + English code-mixing

## ✨ Key Features

- ✅ Offline-capable AI (Ollama)
- ✅ All Indian languages
- ✅ Mixed language support
- ✅ Region & season aware
- ✅ Image analysis with ML
- ✅ Voice input/output
- ✅ Supabase cloud database
- ✅ PWA ready
