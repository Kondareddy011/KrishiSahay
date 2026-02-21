"""
Utility functions for translation and language detection
"""

from typing import Optional

# Simple translation dictionary (replace with actual translation API in production)
TRANSLATION_DICT = {
    # Hindi translations
    "hi": {
        "rice": "चावल",
        "wheat": "गेहूं",
        "pest": "कीट",
        "fertilizer": "उर्वरक",
        "water": "पानी",
        "soil": "मिट्टी"
    },
    # Telugu translations
    "te": {
        "rice": "వరి",
        "wheat": "గోధుమ",
        "pest": "పీడ",
        "fertilizer": "ఎరువు",
        "water": "నీరు",
        "soil": "న ch"
    }
}

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text between languages. For 'mixed' source, returns as-is
    (models handle code-mixing natively).
    """
    if source_lang == target_lang or source_lang == "mixed":
        return text
    # Placeholder - in production use translation API
    return text

def detect_language(text: str) -> str:
    """
    Detect language of input text. Returns 'mixed' if multiple scripts detected.
    Also detects transliterated mixed language (e.g., "ela control cheyam" = Telugu words in English script).
    Supports major Indian languages.
    """
    has_devanagari = any('\u0900' <= c <= '\u097F' for c in text)  # Hindi, Marathi, Sanskrit
    has_telugu = any('\u0C00' <= c <= '\u0C7F' for c in text)
    has_tamil = any('\u0B80' <= c <= '\u0BFF' for c in text)
    has_bengali = any('\u0980' <= c <= '\u09FF' for c in text)  # Bengali, Assamese
    has_gujarati = any('\u0A80' <= c <= '\u0AFF' for c in text)
    has_kannada = any('\u0C80' <= c <= '\u0CFF' for c in text)
    has_malayalam = any('\u0D00' <= c <= '\u0D7F' for c in text)
    has_odia = any('\u0B00' <= c <= '\u0B7F' for c in text)
    has_gurmukhi = any('\u0A00' <= c <= '\u0A7F' for c in text)  # Punjabi
    has_english = any('a' <= c <= 'z' or 'A' <= c <= 'Z' for c in text)
    
    # Check for transliterated Indian language words (common patterns)
    text_lower = text.lower()
    telugu_words = ['ela', 'cheyam', 'undhi', 'ledhu', 'avuthundi', 'cheppu', 'ivvandi']
    hindi_words = ['kaise', 'kya', 'kyun', 'hai', 'ho', 'kar', 'karne', 'ke', 'ki']
    tamil_words = ['elaam', 'irukku', 'pannu', 'pannalam', 'venum', 'illai']
    
    has_transliterated_telugu = any(word in text_lower for word in telugu_words)
    has_transliterated_hindi = any(word in text_lower for word in hindi_words)
    has_transliterated_tamil = any(word in text_lower for word in tamil_words)
    
    scripts = sum([has_devanagari, has_telugu, has_tamil, has_bengali, has_gujarati,
                   has_kannada, has_malayalam, has_odia, has_gurmukhi, has_english])
    
    # Mixed if multiple scripts OR transliterated words + English
    if scripts >= 2:
        return "mixed"
    if has_transliterated_telugu and has_english:
        return "mixed"
    if has_transliterated_hindi and has_english:
        return "mixed"
    if has_transliterated_tamil and has_english:
        return "mixed"
    
    if has_devanagari:
        return "hi"  # Default to Hindi for Devanagari
    if has_telugu:
        return "te"
    if has_tamil:
        return "ta"
    if has_bengali:
        return "bn"
    if has_gujarati:
        return "gu"
    if has_kannada:
        return "kn"
    if has_malayalam:
        return "ml"
    if has_odia:
        return "or"
    if has_gurmukhi:
        return "pa"
    return "en"

def normalize_query(query: str) -> str:
    """Normalize query for caching and search"""
    return query.lower().strip()
