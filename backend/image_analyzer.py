"""
Image Analyzer for Agricultural Images
Analyzes uploaded images of crops, pests, diseases, and fields
Uses ML model for classification when available
"""

import io
import os
from PIL import Image
from typing import Dict, List, Optional
import base64
from datetime import datetime
import gemini_client

class ImageAnalyzer:
    """
    Analyzes agricultural images and provides recommendations.
    Uses pattern matching and heuristics (can be extended with ML models).
    """
    
    def __init__(self):
        self.pest_patterns = {
            'aphid': ['small', 'green', 'insect', 'cluster'],
            'stem_borer': ['hole', 'tunnel', 'yellowing', 'wilting'],
            'leaf_folder': ['folded', 'rolled', 'brown', 'leaf'],
            'rust': ['orange', 'brown', 'spots', 'powdery'],
            'blight': ['brown', 'black', 'spots', 'wilting', 'dead']
        }
        
        self.crop_patterns = {
            'rice': ['paddy', 'green', 'field', 'water'],
            'wheat': ['golden', 'yellow', 'grain', 'stalk'],
            'cotton': ['white', 'boll', 'fiber', 'plant'],
            'maize': ['corn', 'yellow', 'cob', 'tall']
        }
        
        # Load ML model if available
        self.ml_model = None
        try:
            from ml_model import AgriculturalMLModel
            self.ml_model = AgriculturalMLModel(model_type="vit")
            if self.ml_model.load_model():
                print("ML model loaded for image classification")
        except Exception as e:
            print(f"ML model not available: {e}")
    
    def analyze(self, image_data: bytes, filename: str) -> Dict:
        """
        Analyze agricultural image and return recommendations.
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Get image properties
            width, height = image.size
            format_type = image.format
            mode = image.mode
            
            # Try Gemini Vision first (Highest Quality)
            if gemini_client.is_available():
                try:
                    vision_prompt = (
                        "Analyze this agricultural image. "
                        "1. Identify the crop or plant. "
                        "2. Detect any diseases, pests, or nutrient deficiencies. "
                        "3. Provide the CAUSE of the issue. "
                        "4. Provide detailed SOLUTIONS and actions for the farmer. "
                        "Format the response with clear headings: **Detected Issue**, **Cause**, and **Recommendations**."
                    )
                    vision_system_prompt = (
                        "You are an expert plant pathologist and agricultural scientist. "
                        "Provide accurate, actionable advice for Indian farmers. "
                        "Be specific about organic and chemical solutions when appropriate."
                    )
                    
                    gemini_vision_res = gemini_client.analyze_image(
                        image_data=image_data,
                        prompt=vision_prompt,
                        system_prompt=vision_system_prompt
                    )
                    
                    if gemini_vision_res:
                        # Extract basic category for database indexing
                        category = "Disease Detection"
                        if "pest" in gemini_vision_res.lower():
                            category = "Pest Management"
                        elif "healthy" in gemini_vision_res.lower():
                            category = "Crop Health"
                            
                        return {
                            "description": "Analysis powered by Gemini Vision.",
                            "detected_issues": ["See detailed report"],
                            "recommendations": gemini_vision_res,
                            "category": category,
                            "confidence": "high",
                            "source": "gemini_vision"
                        }
                except Exception as e:
                    print(f"Gemini Vision error: {e}")
            
            # Try ML model first if available (Local/Legacy)
            ml_prediction = None
            if self.ml_model and self.ml_model.loaded:
                try:
                    ml_prediction = self.ml_model.predict(image_data)
                    print(f"ML prediction: {ml_prediction.get('primary_category')} (confidence: {ml_prediction.get('confidence', 0):.2f})")
                except Exception as e:
                    print(f"ML prediction error: {e}")
            
            # Analyze image characteristics (fallback/combined)
            analysis = self._analyze_image_properties(image)
            
            # Combine ML predictions with traditional analysis
            if ml_prediction and ml_prediction.get("confidence", 0) > 0.3:
                # Use ML model recommendations if confidence is good
                recommendations = self.ml_model.get_recommendations(ml_prediction)
                category = ml_prediction.get("primary_category", analysis.get("category", "Crop Analysis")).title()
                confidence = "high" if ml_prediction.get("confidence", 0) > 0.7 else "medium"
            else:
                # Use traditional analysis
                recommendations = self._generate_recommendations(analysis, filename)
                category = analysis.get("category", "Crop Analysis")
                confidence = analysis.get("confidence", "medium")
            
            # Combine descriptions
            description = analysis["description"]
            if ml_prediction:
                ml_desc = f"ML model detected: {ml_prediction.get('primary_category', 'unknown')} (confidence: {ml_prediction.get('confidence', 0):.2f})"
                description = f"{description} {ml_desc}"
            
            return {
                "description": description,
                "detected_issues": analysis.get("issues", []),
                "recommendations": recommendations,
                "category": category,
                "confidence": confidence,
                "ml_prediction": ml_prediction if ml_prediction else None
            }
            
        except Exception as e:
            # Fallback analysis
            return self._fallback_analysis(filename)
    
    def _analyze_image_properties(self, image: Image.Image) -> Dict:
        """Analyze image properties and detect patterns"""
        width, height = image.size
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get dominant colors
        colors = image.getcolors(maxcolors=256*256*256)
        if colors:
            # Sort by frequency
            colors = sorted(colors, key=lambda x: x[0], reverse=True)
            dominant_colors = [color[1] for color in colors[:5]]
        else:
            dominant_colors = []
        
        # Analyze color patterns
        green_dominant = self._is_green_dominant(dominant_colors)
        brown_dominant = self._is_brown_dominant(dominant_colors)
        yellow_present = self._has_yellow(dominant_colors)
        
        # Detect issues based on colors and patterns
        issues = []
        if brown_dominant and not green_dominant:
            issues.append("Possible disease or pest damage detected")
        if yellow_present and green_dominant:
            issues.append("Possible nutrient deficiency or early pest infestation")
        
        # Determine category
        if brown_dominant:
            category = "Pest Management"
        elif yellow_present:
            category = "Crop Health"
        else:
            category = "Crop Analysis"
        
        description = self._generate_description(green_dominant, brown_dominant, yellow_present, width, height)
        
        return {
            "description": description,
            "issues": issues,
            "category": category,
            "confidence": "medium",
            "image_size": f"{width}x{height}",
            "dominant_colors": len(dominant_colors)
        }
    
    def _is_green_dominant(self, colors: List) -> bool:
        """Check if green is dominant in image"""
        if not colors:
            return False
        green_count = 0
        for color in colors[:10]:  # Check top 10 colors
            r, g, b = color
            if g > r and g > b and g > 100:  # Green is dominant
                green_count += 1
        return green_count >= 3
    
    def _is_brown_dominant(self, colors: List) -> bool:
        """Check if brown/dark colors are dominant"""
        if not colors:
            return False
        brown_count = 0
        for color in colors[:10]:
            r, g, b = color
            # Brown: low brightness, similar RGB values
            brightness = (r + g + b) / 3
            if brightness < 150 and abs(r - g) < 30 and abs(g - b) < 30:
                brown_count += 1
        return brown_count >= 3
    
    def _has_yellow(self, colors: List) -> bool:
        """Check if yellow is present"""
        if not colors:
            return False
        for color in colors[:10]:
            r, g, b = color
            # Yellow: high red and green, low blue
            if r > 150 and g > 150 and b < 100:
                return True
        return False
    
    def _generate_description(self, green: bool, brown: bool, yellow: bool, width: int, height: int) -> str:
        """Generate description based on analysis"""
        parts = []
        
        if green:
            parts.append("The image shows healthy green vegetation")
        if brown:
            parts.append("Brown or dark areas detected, which may indicate disease or pest damage")
        if yellow:
            parts.append("Yellowing observed, possibly indicating nutrient deficiency or pest infestation")
        
        if not parts:
            parts.append("Agricultural image analyzed")
        
        parts.append(f"Image dimensions: {width}x{height} pixels")
        
        return ". ".join(parts) + "."
    
    def _generate_recommendations(self, analysis: Dict, filename: str) -> str:
        """Generate actionable recommendations based on analysis"""
        issues = analysis.get("issues", [])
        category = analysis.get("category", "Crop Analysis")
        
        recommendations = []
        
        if "disease or pest damage" in str(issues).lower():
            recommendations.append("🔍 **Immediate Actions:**")
            recommendations.append("1. Identify the specific pest or disease by examining the affected areas closely")
            recommendations.append("2. Remove and destroy severely affected plant parts to prevent spread")
            recommendations.append("3. Apply appropriate organic pesticides (neem oil, garlic-chili spray)")
            recommendations.append("4. If using chemical pesticides, follow recommended dosage and safety guidelines")
            recommendations.append("")
            recommendations.append("💡 **Prevention:**")
            recommendations.append("- Maintain proper field hygiene and remove crop residues")
            recommendations.append("- Use resistant crop varieties")
            recommendations.append("- Practice crop rotation")
            recommendations.append("- Monitor fields regularly for early detection")
        
        elif "nutrient deficiency" in str(issues).lower() or "pest infestation" in str(issues).lower():
            recommendations.append("🌱 **Recommended Actions:**")
            recommendations.append("1. Conduct soil test to identify specific nutrient deficiencies")
            recommendations.append("2. Apply balanced NPK fertilizer based on soil test results")
            recommendations.append("3. For pest control, use integrated pest management (IPM) approach")
            recommendations.append("4. Apply neem-based organic pesticides as first line of defense")
            recommendations.append("")
            recommendations.append("📋 **Next Steps:**")
            recommendations.append("- Monitor crop health weekly")
            recommendations.append("- Maintain proper irrigation schedule")
            recommendations.append("- Consult local agricultural extension officer for region-specific advice")
        
        else:
            recommendations.append("✅ **General Recommendations:**")
            recommendations.append("1. Continue regular monitoring of crop health")
            recommendations.append("2. Maintain proper irrigation and drainage")
            recommendations.append("3. Apply fertilizers based on crop growth stage")
            recommendations.append("4. Keep field free from weeds")
            recommendations.append("")
            recommendations.append("💡 **Best Practices:**")
            recommendations.append("- Follow recommended spacing between plants")
            recommendations.append("- Use quality seeds from certified sources")
            recommendations.append("- Maintain field hygiene")
            recommendations.append("- Keep records of crop management practices")
        
        # Add category-specific advice
        if category == "Pest Management":
            recommendations.append("")
            recommendations.append("🐛 **Pest Control Tips:**")
            recommendations.append("- Identify pests accurately before treatment")
            recommendations.append("- Use biological control methods when possible")
            recommendations.append("- Apply pesticides during early morning or evening")
            recommendations.append("- Follow recommended waiting period before harvest")
        
        return "\n".join(recommendations)
    
    def _fallback_analysis(self, filename: str) -> Dict:
        """Fallback analysis when image processing fails"""
        return {
            "description": f"Image '{filename}' received. Analysis in progress.",
            "detected_issues": [],
            "recommendations": (
                "Thank you for uploading the image. Based on agricultural best practices:\n\n"
                "1. **Regular Monitoring**: Check your crops daily for any signs of pests, diseases, or nutrient deficiencies\n"
                "2. **Early Detection**: Early identification of issues helps prevent crop loss\n"
                "3. **Proper Treatment**: Use appropriate organic or chemical treatments based on the specific issue\n"
                "4. **Consult Experts**: Visit your nearest Krishi Vigyan Kendra (KVK) for expert advice\n\n"
                "For more specific recommendations, please describe what you see in the image or consult with an agricultural expert."
            ),
            "category": "General Agriculture",
            "confidence": "low"
        }
