"""
KrishiSahay - FastAPI Backend Server
Main entry point for the agricultural AI assistant API
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime

from database import Database
from utils import translate_text, detect_language
from context_utils import build_context_prompt, get_indian_season
import gemini_client
import openai_client
import ollama_client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="KrishiSahay API",
    description="AI-powered Agricultural Assistant Backend",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
rag_pipeline = None
image_analyzer = None


def _get_mock_answer(query: str) -> dict:
    """Always-available mock answers (no ML deps)."""
    q = query.lower()
    mocks = {
        "rice": ("Rice cultivation requires well-drained soil (pH 5-6.5). Plant June-July. Use 20-25 kg seeds/ha. NPK 100:50:50 in split doses. Keep 5-7 cm water depth.", "Crops & Cultivation"),
        "wheat": ("Wheat: loamy soil pH 6-7.5. Sow Nov-Dec. 100-125 kg seeds/ha. Apply 120 kg N, 60 kg P2O5, 40 kg K2O. Harvest at 20-25% moisture.", "Crops & Cultivation"),
        "pest": ("Use IPM. Identify pests early. Neem-based organic pesticides first. Rotate crops, remove residues, keep field clean.", "Pest Management"),
        "fertilizer": ("Apply NPK based on soil test. 4:2:1 ratio often works. N in split doses: 50% sowing, 25% tillering, 25% flowering. Use compost.", "Fertilizers"),
    }
    for k, (ans, cat) in mocks.items():
        if k in q:
            return {"answer": ans, "category": cat}
    return {
        "answer": f"Thanks for your question about '{query}'. Visit your nearest Krishi Vigyan Kendra (KVK) for region-specific guidance.",
        "category": "General Agriculture",
    }


def _load_rag():
    global rag_pipeline
    try:
        from model import RAGPipeline
        r = RAGPipeline()
        r.load_index()
        rag_pipeline = r
        return True
    except Exception as e:
        print(f"RAG not loaded (using mock): {e}")
        return False


def _load_image_analyzer():
    global image_analyzer
    try:
        from image_analyzer import ImageAnalyzer
        image_analyzer = ImageAnalyzer()
        return True
    except Exception as e:
        print(f"Image analyzer not loaded: {e}")
        return False


def _ollama_answer(query: str, region: Optional[str], season: Optional[str], lat: Optional[float], lon: Optional[float], lang: str) -> Optional[dict]:
    """Try Ollama for generative answer. Returns None if unavailable."""
    try:
        from ollama_client import generate, is_available
        if not is_available():
            return None
        ctx = build_context_prompt(region=region, season=season, lat=lat, lon=lon)
        
        # Enhanced system prompt for mixed languages
        if lang == "mixed":
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                "The user is asking in MIXED LANGUAGE (e.g., Telugu/Hindi + English code-mixing). "
                "IMPORTANT: Respond in the SAME language mix as the user's question. "
                "If they mix Telugu + English, respond in Telugu + English. "
                "If they mix Hindi + English, respond in Hindi + English. "
                "Keep the same code-mixing style. "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        else:
            lang_instruction = {
                "hi": "Respond in Hindi (हिंदी).",
                "te": "Respond in Telugu (తెలుగు).",
                "ta": "Respond in Tamil (தமிழ்).",
                "bn": "Respond in Bengali (বাংলা).",
                "mr": "Respond in Marathi (मराठी).",
                "gu": "Respond in Gujarati (ગુજરાતી).",
                "kn": "Respond in Kannada (ಕನ್ನಡ).",
                "ml": "Respond in Malayalam (മലയാളം).",
                "or": "Respond in Odia (ଓଡ଼ିଆ).",
                "pa": "Respond in Punjabi (ਪੰਜਾਬੀ).",
                "as": "Respond in Assamese (অসমীয়া).",
                "ur": "Respond in Urdu (اردو).",
            }.get(lang, "Respond in English.")
            
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                + lang_instruction + " "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        
        resp = generate(prompt=query, system_prompt=system, temperature=0.3, max_tokens=512)
        if resp:
            return {"answer": resp.strip(), "category": "AI Assistant", "source": "ollama"}
    except Exception as e:
        print(f"Ollama error: {e}")
    return None


def _openai_answer(query: str, region: Optional[str], season: Optional[str], lat: Optional[float], lon: Optional[float], lang: str) -> Optional[dict]:
    """Try OpenAI for generative answer. Returns None if unavailable."""
    try:
        if not openai_client.is_available():
            return None
        ctx = build_context_prompt(region=region, season=season, lat=lat, lon=lon)
        
        # Enhanced system prompt (consistent with Ollama logic)
        if lang == "mixed":
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                "The user is asking in MIXED LANGUAGE (e.g., Telugu/Hindi + English code-mixing). "
                "IMPORTANT: Respond in the SAME language mix as the user's question. "
                "If they mix Telugu + English, respond in Telugu + English. "
                "If they mix Hindi + English, respond in Hindi + English. "
                "Keep the same code-mixing style. "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        else:
            lang_instruction = {
                "hi": "Respond in Hindi (हिंदी).",
                "te": "Respond in Telugu (తెలుగు).",
                "ta": "Respond in Tamil (தமிழ்).",
                "bn": "Respond in Bengali (বাংলা).",
                "mr": "Respond in Marathi (मराठी).",
                "gu": "Respond in Gujarati (ગુજરાતી).",
                "kn": "Respond in Kannada (ಕನ್ನಡ).",
                "ml": "Respond in Malayalam (മലയാളം).",
                "or": "Respond in Odia (ଓଡ଼ିଆ).",
                "pa": "Respond in Punjabi (ਪੰਜਾਬੀ).",
                "as": "Respond in Assamese (অসমীয়া).",
                "ur": "Respond in Urdu (اردو).",
            }.get(lang, "Respond in English.")
            
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                + lang_instruction + " "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        
        resp = openai_client.generate(prompt=query, system_prompt=system, temperature=0.3, max_tokens=512)
        if resp:
            return {"answer": resp.strip(), "category": "AI Assistant", "source": "openai"}
    except Exception as e:
        print(f"OpenAI error: {e}")
    return None


def _gemini_answer(query: str, region: Optional[str], season: Optional[str], lat: Optional[float], lon: Optional[float], lang: str) -> Optional[dict]:
    """Try Gemini for generative answer. Returns None if unavailable."""
    try:
        if not gemini_client.is_available():
            return None
        ctx = build_context_prompt(region=region, season=season, lat=lat, lon=lon)
        
        # Enhanced system prompt
        if lang == "mixed":
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                "The user is asking in MIXED LANGUAGE (e.g., Telugu/Hindi + English code-mixing). "
                "IMPORTANT: Respond in the SAME language mix as the user's question. "
                "If they mix Telugu + English, respond in Telugu + English. "
                "If they mix Hindi + English, respond in Hindi + English. "
                "Keep the same code-mixing style. "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        else:
            lang_instruction = {
                "hi": "Respond in Hindi (हिंदी).",
                "te": "Respond in Telugu (తెలుగు).",
                "ta": "Respond in Tamil (தமிழ்).",
                "bn": "Respond in Bengali (বাংলা).",
                "mr": "Respond in Marathi (मराठी).",
                "gu": "Respond in Gujarati (ગુજરાતી).",
                "kn": "Respond in Kannada (କನ್ನಡ).",
                "ml": "Respond in Malayalam (മലയാളం).",
                "or": "Respond in Odia (ଓଡ଼ିଆ).",
                "pa": "Respond in Punjabi (ਪੰਜਾਬੀ).",
                "as": "Respond in Assamese (অসমীয়া).",
                "ur": "Respond in Urdu (اردو).",
            }.get(lang, "Respond in English.")
            
            system = (
                "You are KrishiSahay, an agricultural assistant for Indian farmers. "
                + lang_instruction + " "
                "Context: " + ctx + " "
                "Give concise, practical agricultural advice."
            )
        
        resp = gemini_client.generate(prompt=query, system_prompt=system, temperature=0.3, max_tokens=512)
        if resp:
            return {"answer": resp.strip(), "category": "AI Assistant", "source": "gemini"}
    except Exception as e:
        print(f"Gemini error: {e}")
    return None


@app.on_event("startup")
async def startup_event():
    print("Initializing KrishiSahay backend...")
    _load_rag()
    _load_image_analyzer()
    try:
        from ollama_client import is_available
        if is_available():
            print("Ollama (offline AI) available")
        else:
            print("Ollama not running - install & run: ollama run llama3.2")
    except Exception:
        pass

    if gemini_client.is_available():
        print(f"Gemini API available (Model: {gemini_client.GEMINI_MODEL})")
    elif openai_client.is_available():
        print(f"OpenAI API available (Model: {openai_client.OPENAI_MODEL})")
    else:
        print("No external AI API configured (GEMINI_API_KEY or OPENAI_API_KEY missing)")

    print("Backend ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    db.close()

# Request/Response Models
class AskRequest(BaseModel):
    query: str
    language: str = "en"  # en, hi, te, ta, bn, mr, gu, kn, ml, or, pa, as, ur, mixed, auto
    region: Optional[str] = None
    season: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class AskResponse(BaseModel):
    answer: str
    source: str  # local, cache, offline
    category: Optional[str] = None

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    feedback: str  # positive, negative

class AppFeedbackRequest(BaseModel):
    message: str
    rating: Optional[int] = None  # 1-5 optional
    page: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "KrishiSahay API",
        "version": "1.0.0"
    }

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Main endpoint for agricultural questions.
    Supports: Ollama (offline AI), RAG, mock. Region/season-aware. Mixed-language.
    """
    try:
        lang = request.language
        if lang == "auto" or lang == "mixed":
            detected = detect_language(request.query)
            if lang == "mixed" or detected == "mixed":
                lang = "mixed"
            elif lang == "auto":
                lang = detected

        region = request.region
        season = request.season or get_indian_season()
        lat, lon = request.lat, request.lon

        cached_response = db.get_cached_response(request.query, lang)
        if cached_response:
            return AskResponse(
                answer=cached_response["answer"],
                source="cache",
                category=cached_response.get("category"),
            )

        # Mixed language: pass query as-is (no translation)
        # For mixed language, preserve the original query exactly
        query_for_model = request.query
        if lang not in ("mixed", "en", "auto"):
            # Try translation, but if it fails, use original
            query_for_model = translate_text(request.query, lang, "en")
            if query_for_model == request.query and lang != "en":
                query_for_model = request.query

        result = _get_mock_answer(query_for_model)

        # 1. Try Gemini (Primary)
        gemini_out = _gemini_answer(
            query_for_model, region, season, lat, lon, lang
        )
        if gemini_out:
            result = gemini_out
        else:
            # 2. Try OpenAI (Secondary)
            openai_out = _openai_answer(
                query_for_model, region, season, lat, lon, lang
            )
            if openai_out:
                result = openai_out
            else:
                # 3. Try Ollama (Offline)
                ollama_out = _ollama_answer(
                    query_for_model, region, season, lat, lon, lang
                )
                if ollama_out:
                    result = ollama_out
                
                # 4. Try RAG if no generative models returned
                elif rag_pipeline and rag_pipeline.index_loaded:
                    try:
                        ctx = build_context_prompt(region, season, lat, lon)
                        # For mixed language, add explicit instruction to RAG
                        if lang == "mixed":
                            rag_query = f"User question (mixed language): {query_for_model}. Context: {ctx}. Provide answer in the same language mix."
                        else:
                            rag_query = f"{query_for_model}. Context: {ctx}" if ctx else query_for_model
                        rag_result = rag_pipeline.query(rag_query, top_k=3)
                        if rag_result and rag_result.get("answer"):
                            result = rag_result
                    except Exception as e:
                        print(f"RAG query error: {e}")

        answer = result["answer"]

        # Don't translate if language is mixed or if AI already handled it
        if lang not in ("en", "mixed", "auto") and result.get("source") not in ("ollama", "openai", "gemini"):
            answer = translate_text(result["answer"], "en", lang)

        db.cache_response(
            query=request.query,
            language=lang,
            answer=answer,
            category=result.get("category"),
        )

        return AskResponse(
            answer=answer,
            source=result.get("source", "local"),
            category=result.get("category"),
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ask error: {e}")
        fallback = _get_mock_answer(request.query)
        return AskResponse(
            answer=fallback["answer"],
            source="local",
            category=fallback.get("category"),
        )

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Store user feedback for improving responses"""
    try:
        db.save_feedback(
            query=feedback.query,
            answer=feedback.answer,
            feedback=feedback.feedback
        )
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/app-feedback")
async def submit_app_feedback(payload: AppFeedbackRequest):
    """Store general app feedback (rating + message)."""
    try:
        if not payload.message or payload.message.strip() == "":
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        if payload.rating is not None and (payload.rating < 1 or payload.rating > 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

        db.save_app_feedback(
            message=payload.message.strip(),
            rating=payload.rating,
            page=payload.page,
        )
        return {"status": "success", "message": "App feedback recorded"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/app-feedback")
async def get_app_feedback(limit: int = 20):
    """Fetch recent app feedback."""
    try:
        safe_limit = max(1, min(int(limit), 100))
        data = db.get_recent_app_feedback(limit=safe_limit)
        return {"items": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image", response_model=AskResponse)
async def analyze_image(
    image: UploadFile = File(...),
    language: str = Form("en"),
    query: Optional[str] = Form(None)
):
    """
    Analyze uploaded agricultural image (crops, pests, diseases, fields).
    """
    try:
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        image_data = await image.read()

        if not image_analyzer:
            raise HTTPException(status_code=503, detail="Image analysis not available. Install Pillow.")

        analysis_result = image_analyzer.analyze(image_data, image.filename or "image")
        
        # If user provided context query, combine with analysis
        if query and rag_pipeline and rag_pipeline.index_loaded:
            try:
                combined_query = f"{analysis_result['description']}. {query}"
                rag_result = rag_pipeline.query(combined_query, top_k=3)
                answer = rag_result["answer"]
                category = rag_result.get("category", analysis_result.get("category"))
            except Exception:
                answer = analysis_result["recommendations"]
                category = analysis_result.get("category", "Crop Analysis")
        else:
            # Use analysis recommendations
            answer = analysis_result["recommendations"]
            category = analysis_result.get("category", "Crop Analysis")
        
        # Translate answer if needed
        if language != "en":
            answer = translate_text(answer, "en", language)
        
        # Save image analysis to Supabase
        db.save_image_analysis(
            image_filename=image.filename or "image",
            analysis_result=analysis_result,
            language=language,
            user_query=query,
            recommendations=answer,
            category=category
        )
        
        return AskResponse(
            answer=answer,
            source="image_analysis",
            category=category
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")

@app.get("/health")
async def health_check():
    ollama_ok = False
    try:
        from ollama_client import is_available
        ollama_ok = is_available()
    except Exception:
        pass
    return {
        "status": "healthy",
        "rag_index_loaded": rag_pipeline.index_loaded if rag_pipeline else False,
        "ollama_available": ollama_ok,
        "openai_available": openai_client.is_available(),
        "gemini_available": gemini_client.is_available(),
        "database_connected": db.is_connected(),
        "timestamp": datetime.now().isoformat(),
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
