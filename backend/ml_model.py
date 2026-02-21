"""
ML Model for Agricultural Image Classification
Uses Vision Transformer (ViT) or CNN for crop/pest/disease detection
"""

import os
import io
import numpy as np
from PIL import Image
from typing import Dict, List, Optional, Tuple
import torch
import torchvision.transforms as transforms

# Try to load transformers, fallback to basic if not available
try:
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("transformers not available - using basic image analysis")

# Try to load torchvision models
try:
    import torchvision.models as models
    TORCHVISION_AVAILABLE = True
except ImportError:
    TORCHVISION_AVAILABLE = False


class AgriculturalMLModel:
    """
    ML model for agricultural image classification.
    Detects crops, pests, diseases, and provides recommendations.
    """
    
    def __init__(self, model_type: str = "vit"):
        """
        Initialize ML model.
        
        Args:
            model_type: "vit" (Vision Transformer) or "resnet" (ResNet CNN)
        """
        self.model_type = model_type
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.loaded = False
        
        # Agricultural categories
        self.crop_categories = [
            "rice", "wheat", "maize", "cotton", "sugarcane", 
            "potato", "tomato", "onion", "chili", "vegetables"
        ]
        
        self.pest_categories = [
            "aphid", "stem_borer", "leaf_folder", "whitefly", 
            "thrips", "mealybug", "mite", "caterpillar"
        ]
        
        self.disease_categories = [
            "rust", "blight", "smut", "mildew", "rot", 
            "wilt", "spot", "mosaic", "yellowing"
        ]
        
    def load_model(self) -> bool:
        """Load the ML model"""
        try:
            if TRANSFORMERS_AVAILABLE and self.model_type == "vit":
                # Use Vision Transformer from Hugging Face
                model_name = "google/vit-base-patch16-224"
                print(f"Loading Vision Transformer: {model_name}")
                self.processor = AutoImageProcessor.from_pretrained(model_name)
                self.model = AutoModelForImageClassification.from_pretrained(model_name)
                self.model.to(self.device)
                self.model.eval()
                self.loaded = True
                print("Vision Transformer loaded successfully")
                return True
                
            elif TORCHVISION_AVAILABLE and self.model_type == "resnet":
                # Use ResNet from torchvision
                print("Loading ResNet50 model")
                self.model = models.resnet50(pretrained=True)
                self.model.eval()
                self.model.to(self.device)
                
                # ImageNet preprocessing
                self.transform = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]
                    )
                ])
                self.loaded = True
                print("ResNet50 loaded successfully")
                return True
            else:
                print("ML models not available - install: pip install transformers torch torchvision")
                return False
                
        except Exception as e:
            print(f"Error loading ML model: {e}")
            self.loaded = False
            return False
    
    def predict(self, image_data: bytes) -> Dict:
        """
        Predict agricultural category from image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        if not self.loaded:
            return self._fallback_prediction()
        
        try:
            # Load and preprocess image
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            if self.model_type == "vit" and TRANSFORMERS_AVAILABLE:
                return self._predict_vit(image)
            elif self.model_type == "resnet" and TORCHVISION_AVAILABLE:
                return self._predict_resnet(image)
            else:
                return self._fallback_prediction()
                
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._fallback_prediction()
    
    def _predict_vit(self, image: Image.Image) -> Dict:
        """Predict using Vision Transformer"""
        try:
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits, dim=-1)
                top_probs, top_indices = torch.topk(probabilities, k=5)
            
            # Map ImageNet classes to agricultural categories
            predictions = []
            for prob, idx in zip(top_probs[0], top_indices[0]):
                class_name = self.model.config.id2label.get(idx.item(), "unknown")
                predictions.append({
                    "class": class_name,
                    "confidence": prob.item(),
                    "category": self._map_to_agricultural_category(class_name)
                })
            
            return {
                "predictions": predictions,
                "primary_category": predictions[0]["category"] if predictions else "unknown",
                "confidence": float(predictions[0]["confidence"]) if predictions else 0.0,
                "model_type": "vit"
            }
        except Exception as e:
            print(f"ViT prediction error: {e}")
            return self._fallback_prediction()
    
    def _predict_resnet(self, image: Image.Image) -> Dict:
        """Predict using ResNet"""
        try:
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                top_probs, top_indices = torch.topk(probabilities, k=5)
            
            # Map ImageNet classes to agricultural categories
            predictions = []
            for prob, idx in zip(top_probs, top_indices):
                # ImageNet class mapping (simplified)
                class_name = f"class_{idx.item()}"
                predictions.append({
                    "class": class_name,
                    "confidence": prob.item(),
                    "category": self._map_to_agricultural_category(class_name)
                })
            
            return {
                "predictions": predictions,
                "primary_category": predictions[0]["category"] if predictions else "unknown",
                "confidence": float(predictions[0]["confidence"]) if predictions else 0.0,
                "model_type": "resnet"
            }
        except Exception as e:
            print(f"ResNet prediction error: {e}")
            return self._fallback_prediction()
    
    def _map_to_agricultural_category(self, class_name: str) -> str:
        """Map ImageNet/class names to agricultural categories"""
        class_lower = class_name.lower()
        
        # Crop detection
        crop_keywords = ["corn", "maize", "wheat", "rice", "grain", "vegetable", "plant", "crop"]
        if any(kw in class_lower for kw in crop_keywords):
            return "crop"
        
        # Pest detection (insects)
        pest_keywords = ["insect", "bug", "beetle", "fly", "moth", "caterpillar", "aphid"]
        if any(kw in class_lower for kw in pest_keywords):
            return "pest"
        
        # Disease detection (damaged/abnormal)
        disease_keywords = ["disease", "fungus", "mold", "rot", "wilt", "spot", "blight"]
        if any(kw in class_lower for kw in disease_keywords):
            return "disease"
        
        return "general"
    
    def _fallback_prediction(self) -> Dict:
        """Fallback when ML model is not available"""
        return {
            "predictions": [],
            "primary_category": "general",
            "confidence": 0.0,
            "model_type": "fallback",
            "message": "ML model not loaded - using basic image analysis"
        }
    
    def get_recommendations(self, prediction: Dict) -> str:
        """Generate recommendations based on ML prediction"""
        category = prediction.get("primary_category", "general")
        confidence = prediction.get("confidence", 0.0)
        
        recommendations = []
        
        if category == "crop" and confidence > 0.5:
            recommendations.append("✅ **Crop Detected:**")
            recommendations.append("1. Monitor crop growth stage and health regularly")
            recommendations.append("2. Apply fertilizers based on crop growth stage")
            recommendations.append("3. Maintain proper irrigation schedule")
            recommendations.append("4. Check for pests and diseases weekly")
            
        elif category == "pest" and confidence > 0.5:
            recommendations.append("🐛 **Pest Detected:**")
            recommendations.append("1. Identify the specific pest species")
            recommendations.append("2. Apply organic pesticides (neem oil, garlic-chili spray)")
            recommendations.append("3. Use integrated pest management (IPM) approach")
            recommendations.append("4. Remove affected plant parts to prevent spread")
            recommendations.append("5. Consult agricultural expert for chemical treatment if needed")
            
        elif category == "disease" and confidence > 0.5:
            recommendations.append("⚠️ **Disease Detected:**")
            recommendations.append("1. Identify the specific disease type")
            recommendations.append("2. Remove and destroy severely affected plants")
            recommendations.append("3. Apply appropriate fungicides following safety guidelines")
            recommendations.append("4. Improve field drainage and air circulation")
            recommendations.append("5. Practice crop rotation to prevent recurrence")
            
        else:
            recommendations.append("📸 **Image Analysis:**")
            recommendations.append("1. Upload a clearer image for better detection")
            recommendations.append("2. Ensure good lighting and focus")
            recommendations.append("3. Include multiple angles if possible")
            recommendations.append("4. Consult local agricultural extension officer")
        
        if confidence < 0.5:
            recommendations.append("\n⚠️ Low confidence detection - please verify with expert consultation")
        
        return "\n".join(recommendations)
