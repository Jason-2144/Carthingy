from typing import Dict, Any, List
from datetime import datetime

class FraudAndQualityDetector:
    def __init__(self):
        self.suspicious_keywords = ["urgent sale", "leaving country", "need cash", "wire transfer"]
        
    def score_listing_quality(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        score = 100
        flags = []
        
        # 1. Missing crucial data
        if not listing.get("price") or float(listing.get("price", 0)) < 10000:
            score -= 30
            flags.append("Suspiciously low or missing price")
            
        if not listing.get("km_driven"):
            score -= 10
            flags.append("Missing mileage")
            
        # 2. Description checks
        desc = str(listing.get("description", "")).lower()
        if len(desc) < 20:
            score -= 10
            flags.append("Description too short")
            
        for keyword in self.suspicious_keywords:
            if keyword in desc:
                score -= 15
                flags.append(f"Suspicious keyword found: '{keyword}'")
                
        # 3. Image checks (Assuming we have image metadata)
        image_count = len(listing.get("images", []))
        if image_count == 0:
            score -= 20
            flags.append("No images provided")
        elif image_count < 3:
            score -= 5
            flags.append("Few images provided")
            
        return {
            "quality_score": max(0, score),
            "is_suspicious": score < 50,
            "flags": flags
        }
        
    def detect_duplicate(self, new_listing: Dict[str, Any], existing_listings: List[Dict[str, Any]]) -> bool:
        """
        Simple heuristic: Same Title, Price, Year, and City
        In production, we'd use Image Hashing (pHash) and fuzzy text matching.
        """
        for ext in existing_listings:
            if (ext.get("title") == new_listing.get("title") and 
                ext.get("price") == new_listing.get("price") and 
                ext.get("registration_city") == new_listing.get("registration_city")):
                return True
        return False

fraud_detector = FraudAndQualityDetector()
