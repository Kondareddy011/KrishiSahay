"""
Region, season, and weather context for India.
"""

from datetime import datetime
from typing import Optional, Tuple

# Indian seasons: Kharif (monsoon), Rabi (winter), Zaid (summer)
def get_indian_season() -> str:
    month = datetime.now().month
    if 6 <= month <= 10:
        return "Kharif (monsoon)"
    if month in (11, 12, 1, 2, 3):
        return "Rabi (winter)"
    return "Zaid (summer)"


def get_indian_season_short() -> str:
    month = datetime.now().month
    if 6 <= month <= 10:
        return "kharif"
    if month in (11, 12, 1, 2, 3):
        return "rabi"
    return "zaid"


# Indian state/region -> primary language (for responses)
REGION_LANGUAGE = {
    "andhra pradesh": "te",
    "telangana": "te",
    "tamil nadu": "ta",
    "kerala": "ml",
    "karnataka": "kn",
    "maharashtra": "mr",
    "gujarat": "gu",
    "rajasthan": "hi",
    "uttar pradesh": "hi",
    "madhya pradesh": "hi",
    "bihar": "hi",
    "west bengal": "bn",
    "odisha": "or",
    "punjab": "pa",
    "haryana": "hi",
    "delhi": "hi",
    "uttarakhand": "hi",
    "himachal pradesh": "hi",
    "jharkhand": "hi",
    "chhattisgarh": "hi",
    "assam": "as",
    "goa": "en",
}


def region_to_language(region: Optional[str]) -> str:
    """Map Indian region/state name to language code."""
    if not region or not region.strip():
        return "en"
    key = region.lower().strip()
    return REGION_LANGUAGE.get(key, "en")


def build_context_prompt(
    region: Optional[str] = None,
    season: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> str:
    """Build context string for AI prompt."""
    parts = []
    if region:
        parts.append(f"Region: {region}")
    season_used = season or get_indian_season()
    parts.append(f"Current season in India: {season_used}")
    if lat is not None and lon is not None:
        parts.append(f"Approximate location: {lat:.2f}, {lon:.2f}")
    return ". ".join(parts) if parts else "India (region and season not specified)."
