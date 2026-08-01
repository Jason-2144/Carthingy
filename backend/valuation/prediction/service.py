import pandas as pd
import numpy as np
import os
from backend.valuation.features.extractor import FeatureExtractor
from backend.valuation.models.lgbm_model import LightGBMValuationModel

class PredictionService:
    def __init__(self, model_dir: str = "/tmp/valuation_models"):
        self.model_dir = model_dir
        self.extractor = FeatureExtractor(model_dir=self.model_dir)
        self.model = None

    def load_model(self):
        latest_path = os.path.join(self.model_dir, "model_latest.joblib")
        if not os.path.exists(latest_path):
            raise RuntimeError("No trained model found.")
        self.model = LightGBMValuationModel.load(latest_path)
        self.extractor.load_encoders()

    def predict(self, vehicle_data: dict) -> dict:
        if self.model is None:
            self.load_model()
            
        df = pd.DataFrame([vehicle_data])
        df = self.extractor.extract_features(df)
        X = self.extractor.transform(df)
        
        pred_log = self.model.predict(X)[0]
        estimated_price = float(np.expm1(pred_log))
        
        # Calculate confidence interval based on a heuristic/historical MAPE (e.g. 8%)
        margin = estimated_price * 0.08
        
        return {
            "estimated_market_value": round(estimated_price, 2),
            "expected_price_range": {
                "min": round(estimated_price - margin, 2),
                "max": round(estimated_price + margin, 2)
            },
            "confidence_score": 8.5, # Example constant or calculate based on density
            "factors": self._get_factors(X)
        }
        
    def _get_factors(self, X: pd.DataFrame) -> list:
        # Dummy factors implementation, in real life use SHAP or tree path
        importance = self.model.feature_importance()
        sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        top_features = [k for k, v in sorted_imp[:3]]
        
        factors = []
        for feat in top_features:
            val = X[feat].iloc[0]
            factors.append(f"{feat.replace('_', ' ').title()}: {val}")
        return factors

prediction_service = PredictionService()
