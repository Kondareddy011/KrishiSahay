"""
Sample Agricultural Dataset
Contains agricultural knowledge documents for RAG pipeline
"""

documents = [
    "Brown spots on paddy leaves indicate fungal infection. Use carbendazim fungicide.",
    "For pest control in cotton, use neem oil spray every 7 days.",
    "Urea fertilizer should be applied in split doses for better yield.",
    "PM-KISAN scheme provides financial support to farmers.",
    "Yellow leaves in plants may indicate nitrogen deficiency.",
    "Rice cultivation requires well-drained soil with pH 5-6.5. Plant during monsoon season.",
    "Wheat grows best in loamy soil with pH 6-7.5. Sow in November-December.",
    "Stem borer attacks rice crops. Use cartap hydrochloride or chlorantraniliprole.",
    "Aphids can be controlled using neem-based organic pesticides.",
    "Apply NPK fertilizer in ratio 4:2:1 for most crops.",
    "Integrated Pest Management (IPM) combines biological, cultural, and chemical methods.",
    "Crop rotation helps prevent pest buildup and improves soil health.",
    "Drip irrigation saves water and improves fertilizer efficiency.",
    "Soil testing should be done before applying fertilizers.",
    "Organic farming uses compost, vermicompost, and green manure.",
    "Paddy fields need 5-7 cm water depth during growth period.",
    "Harvest wheat when grain moisture is 20-25%.",
    "Use certified seeds from reliable sources for better yield.",
    "Weed control is essential in first 30-40 days after sowing.",
    "Monitor crops weekly for early pest and disease detection."
]

# Document metadata (optional)
document_metadata = [
    {"category": "Disease Management", "crop": "rice"},
    {"category": "Pest Management", "crop": "cotton"},
    {"category": "Fertilizers", "crop": "general"},
    {"category": "Government Schemes", "crop": "general"},
    {"category": "Nutrient Management", "crop": "general"},
    {"category": "Crop Cultivation", "crop": "rice"},
    {"category": "Crop Cultivation", "crop": "wheat"},
    {"category": "Pest Management", "crop": "rice"},
    {"category": "Pest Management", "crop": "general"},
    {"category": "Fertilizers", "crop": "general"},
    {"category": "Pest Management", "crop": "general"},
    {"category": "Soil Management", "crop": "general"},
    {"category": "Irrigation", "crop": "general"},
    {"category": "Soil Management", "crop": "general"},
    {"category": "Organic Farming", "crop": "general"},
    {"category": "Crop Cultivation", "crop": "rice"},
    {"category": "Crop Cultivation", "crop": "wheat"},
    {"category": "Seed Management", "crop": "general"},
    {"category": "Weed Management", "crop": "general"},
    {"category": "Crop Monitoring", "crop": "general"}
]
