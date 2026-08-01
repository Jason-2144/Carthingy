import pandas as pd
import numpy as np
import datetime
import os
import uuid
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine

from backend.valuation.features.extractor import FeatureExtractor
from backend.valuation.models.lgbm_model import LightGBMValuationModel

class TrainingPipeline:
    def __init__(self, model_dir: str = "/tmp/valuation_models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.extractor = FeatureExtractor(model_dir=self.model_dir)

    async def fetch_data(self) -> pd.DataFrame:
        query = """
            SELECT 
                l.price, l.registration_year, l.km_driven, l.ownership,
                l.fuel, l.transmission, l.colour, l.registration_state, l.registration_city,
                l.first_seen, 
                EXTRACT(DAY FROM (COALESCE(l.last_seen, NOW()) - l.first_seen)) as days_on_market,
                (SELECT COUNT(*) FROM history h WHERE h.listing_id = l.id) as price_drop_count,
                s.type as seller_type,
                c.make, c.model, c.variant, c.body_type
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            LEFT JOIN sellers s ON l.seller_id = s.id
            WHERE l.price IS NOT NULL AND l.km_driven IS NOT NULL AND l.registration_year IS NOT NULL
            LIMIT 500000;
        """
        async with engine.connect() as conn:
            result = await conn.execute(text(query))
            rows = result.fetchall()
            cols = result.keys()
            df = pd.DataFrame([dict(zip(cols, row)) for row in rows])
        return df

    async def run(self) -> dict:
        print("Fetching data...")
        df = await self.fetch_data()
        if df.empty:
            raise ValueError("No data found for training.")

        print("Extracting features...")
        df = self.extractor.extract_features(df)
        X, y = self.extractor.fit_transform(df)

        print("Splitting data...")
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training model...")
        model = LightGBMValuationModel()
        model.train(X_train, y_train, X_val, y_val)

        print("Evaluating...")
        preds_log = model.predict(X_val)
        preds = np.expm1(preds_log)
        y_val_real = np.expm1(y_val)

        mae = mean_absolute_error(y_val_real, preds)
        mape = mean_absolute_percentage_error(y_val_real, preds)
        r2 = r2_score(y_val_real, preds)

        metrics = {
            "mae": float(mae),
            "mape": float(mape),
            "r2": float(r2),
            "timestamp": datetime.datetime.now().isoformat()
        }

        print("Saving model...")
        version = str(uuid.uuid4())[:8]
        model_path = os.path.join(self.model_dir, f"model_{version}.joblib")
        model.save(model_path)
        
        # Link latest
        latest_path = os.path.join(self.model_dir, "model_latest.joblib")
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(model_path, latest_path)
        
        # Save metrics
        with open(os.path.join(self.model_dir, f"metrics_{version}.json"), "w") as f:
            json.dump(metrics, f)

        print("Training pipeline finished.")
        return {"version": version, "metrics": metrics}

