# KrishiSahay - AI-Powered Agricultural Assistant

A full-stack, production-ready web application that helps Indian farmers with agricultural queries. Features multilingual support (all major Indian languages), offline-capable AI, mixed-language understanding, region/season-aware responses, and image analysis.

## 🌾 Features

### Core Features
- **AI-Powered Responses**: Multiple AI backends (Ollama offline AI, RAG pipeline, mock fallback)
- **All Indian Languages**: Hindi, Telugu, Tamil, Bengali, Marathi, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu, English
- **Mixed Language Support**: Understands code-mixing (e.g., Telugu + English, Hindi + English)
- **Region & Season Aware**: Automatically adapts answers based on user's location and current season (Kharif/Rabi/Zaid)
- **Offline Capable**: Works with Ollama (local LLM) for offline AI responses
- **Image Analysis**: Upload crop/pest/disease images for ML-powered analysis
- **Voice Input**: Browser-based speech recognition
- **Text-to-Speech**: Listen to answers in your language
- **Fast Response**: <2 seconds average response time with caching

### Advanced Features
- **Supabase Integration**: Cloud database with MySQL fallback
- **RAG Pipeline**: FAISS vector search with Sentence Transformers
- **ML Model Repository**: Separate repository for advanced ML models
- **PWA Ready**: Installable on mobile devices
- **Offline Caching**: Responses cached for offline access

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** (build tool)
- **Tailwind CSS** (styling)
- **Lucide React** (icons)
- **Supabase JS** (database client)

### Backend
- **FastAPI** (async Python web framework)
- **Ollama** (offline-capable local LLM)
- **FAISS** (vector similarity search)
- **Sentence Transformers** (embeddings)
- **Supabase** (primary database) with MySQL fallback
- **Pillow** (image processing)
- **Transformers** (ML models)

## 📋 Prerequisites

- **Node.js 18+** and npm
- **Python 3.7+** (3.8+ recommended for ML features)
- **pip** (Python package manager)
- **Ollama** (optional, for offline AI) - [Install Ollama](https://ollama.ai)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (optional)
# Copy backend/.env.example to backend/.env and fill in Supabase credentials

# Start the backend server
python main.py
```

The backend will run on `http://localhost:8000`

**Optional: Setup Ollama for Offline AI**
```bash
# Install Ollama from https://ollama.ai
# Then run:
ollama run llama3.2
# Or: ollama run mistral
```

### 3. Frontend Setup

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install

# Configure environment variables
# Copy .env.example to .env and fill in:
# - VITE_SUPABASE_URL
# - VITE_SUPABASE_ANON_KEY
# - VITE_API_URL=/api (for dev proxy)

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173` (or next available port)

### 4. Access the Application

Open your browser and navigate to `http://localhost:5173`

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── model.py                # RAG pipeline with FAISS
│   ├── database.py             # Supabase/MySQL database manager
│   ├── utils.py                # Translation & language detection
│   ├── context_utils.py        # Region/season utilities
│   ├── ollama_client.py        # Offline AI client
│   ├── ml_model.py             # ML model for image classification
│   ├── image_analyzer.py       # Image analysis with ML
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create from .env.example)
│   └── data/
│       └── agricultural_knowledge.json
├── ml-model-repo/              # Separate ML model repository
│   ├── data.py                 # Agricultural knowledge dataset
│   ├── model.py                # FAISS index builder
│   ├── query.py                # Query system
│   ├── rag_pipeline.py        # Full RAG pipeline
│   ├── model_simple.py         # Simple version (no FAISS)
│   ├── query_simple.py         # Simple query (numpy-based)
│   └── rag_simple.py           # Simple RAG (template-based)
├── supabase/
│   └── migrations/             # Database migrations
├── src/
│   ├── components/             # React components
│   ├── pages/                  # Page components
│   ├── services/               # API service layer
│   ├── hooks/                  # Custom React hooks
│   └── App.tsx                 # Main app component
├── public/
│   ├── manifest.json           # PWA manifest
│   └── sw.js                   # Service worker
├── .env                        # Frontend environment variables
└── package.json                # Node.js dependencies
```

## 🔧 Configuration

### Environment Variables

**Frontend** (`.env` in project root):
```env
# API base URL - use /api in dev (proxied to backend)
VITE_API_URL=/api

# Supabase (for frontend + backend)
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Backend** (`backend/.env`):
```env
# Supabase (primary database)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
# Or: SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# MySQL (fallback when Supabase not configured)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=krishisahay

# Offline AI (Ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### Supabase Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Run migration: Copy `supabase/migrations/20260220020000_create_krishisahay_tables.sql` to Supabase SQL Editor and execute
3. Add credentials to `.env` files

See `SUPABASE_SETUP.md` for detailed instructions.

## 📚 API Endpoints

### POST /ask
Ask an agricultural question with region/season context.

**Request:**
```json
{
  "query": "How to control pests in rice?",
  "language": "en",
  "region": "Telangana",
  "season": "Kharif",
  "lat": 17.3850,
  "lon": 78.4867
}
```

**Response:**
```json
{
  "answer": "For pest control in rice during Kharif season in Telangana...",
  "source": "ollama",
  "category": "Pest Management"
}
```

### POST /analyze-image
Analyze agricultural image (crops, pests, diseases).

**Request:** Multipart form data with `image`, `language`, `query` (optional)

**Response:**
```json
{
  "answer": "ML model detected: pest (confidence: 0.85)...",
  "source": "image_analysis",
  "category": "Pest Management"
}
```

### POST /feedback
Submit feedback on an answer.

### POST /app-feedback
Submit general app feedback with rating.

### GET /health
Health check endpoint with system status.

## 🌍 Language Support

### Supported Languages
- **English** (en)
- **Hindi** (hi) - हिंदी
- **Telugu** (te) - తెలుగు
- **Tamil** (ta) - தமிழ்
- **Bengali** (bn) - বাংলা
- **Marathi** (mr) - मराठी
- **Gujarati** (gu) - ગુજરાતી
- **Kannada** (kn) - ಕನ್ನಡ
- **Malayalam** (ml) - മലയാളം
- **Odia** (or) - ଓଡ଼ିଆ
- **Punjabi** (pa) - ਪੰਜਾਬੀ
- **Assamese** (as) - অসমীয়া
- **Urdu** (ur) - اردو
- **Mixed** - Any Indian language + English code-mixing

### Mixed Language Examples
- "rice pests ela control cheyam" (Telugu + English)
- "कीट कैसे control करें" (Hindi + English)
- "paddy lo diseases ela prevent cheyam" (Telugu + English)

## 🧪 Testing

### Test Backend

```bash
cd backend
python main.py
# In another terminal:
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "How to grow rice?", "language": "en"}'
```

### Test Frontend

```bash
npm run dev
# Open http://localhost:5173
```

### Test ML Model Repository

```bash
cd ml-model-repo
python model_simple.py
python query_simple.py
python rag_simple.py
```

## 🐳 Docker Support (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t krishisahay-backend .
docker run -p 8000:8000 krishisahay-backend
```

## 📱 PWA Installation

1. Open the application in a mobile browser
2. Look for "Add to Home Screen" option
3. Install the app
4. The app will work offline with cached responses

## 🔍 Troubleshooting

### Backend Issues

**FAISS index not found:**
- Not required - system uses mock/RAG/Ollama fallback
- To build: `cd backend && python setup_faiss.py`

**Ollama not working:**
- Install Ollama from https://ollama.ai
- Run: `ollama run llama3.2`
- Check: `curl http://localhost:11434/api/tags`

**Port already in use:**
- Change port in `backend/main.py` or kill process using port 8000

**Supabase connection failed:**
- Check `.env` files have correct credentials
- Verify migration ran successfully
- System falls back to MySQL if Supabase unavailable

### Frontend Issues

**API connection failed:**
- Ensure backend is running on port 8000
- Check `VITE_API_URL` in `.env` file (use `/api` for dev)
- Check CORS settings in `backend/main.py`

**Service Worker not working:**
- Clear browser cache
- Check browser console for errors
- Ensure HTTPS in production

## 🚀 Production Deployment

### Backend

1. Use a production ASGI server:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Set up reverse proxy (nginx/Apache)
3. Configure environment variables
4. Use Supabase (already configured) or PostgreSQL

### Frontend

1. Build for production:
```bash
npm run build
```

2. Serve `dist/` folder with a web server
3. Ensure HTTPS for PWA features
4. Update `VITE_API_URL` to production backend URL

## 📝 Adding More Knowledge

To add more agricultural knowledge:

1. Edit `backend/data/agricultural_knowledge.json`
2. Add new documents in the same format
3. Rebuild FAISS index (optional): `cd backend && python setup_faiss.py`
4. Or use Ollama/RAG which doesn't require rebuilding

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Ollama** for offline-capable AI
- **Sentence Transformers** for embeddings
- **FAISS** for efficient vector search
- **FastAPI** for the async backend framework
- **React and Vite** for the frontend framework
- **Supabase** for database infrastructure

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for Indian farmers**
