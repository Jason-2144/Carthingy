import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import joblib
import os
import datetime

class FeatureExtractor:
    def __init__(self, model_dir: str = "/tmp/valuation_models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.cat_cols = [
            'make', 'model', 'variant', 'fuel', 'transmission', 
            'body_type', 'registration_city', 'registration_state', 'seller_type'
        ]
        self.num_cols = ['registration_year', 'km_driven', 'ownership', 'days_on_market', 'price_drop_count']

    def load_encoders(self):
        try:
            self.encoders = joblib.load(f"{self.model_dir}/encoders.joblib")
            self.median_values = joblib.load(f"{self.model_dir}/median_values.joblib")
            return True
        except FileNotFoundError:
            return False

    def fit_transform(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        # Handle Missing values
        self.median_values = df[self.num_cols].median().to_dict()
        df[self.num_cols] = df[self.num_cols].fillna(value=self.median_values)

        for col in self.cat_cols:
            if col not in df.columns:
                df[col] = 'UNKNOWN'
            df[col] = df[col].fillna('UNKNOWN').astype(str).str.upper()

        # Handle Outliers for km_driven and price
        if 'price' in df.columns:
            df = df[df['price'] > 50000]
            df = df[df['price'] < 20000000]
            
        df = df[df['km_driven'] < 500000]

        # Target variable
        y = np.log1p(df['price']) if 'price' in df.columns else None

        # Categorical encoding
        self.encoders = {}
        for col in self.cat_cols:
            df[col] = df[col].astype('category')
            self.encoders[col] = dict(enumerate(df[col].cat.categories))
            
        # Save artifacts
        joblib.dump(self.encoders, f"{self.model_dir}/encoders.joblib")
        joblib.dump(self.median_values, f"{self.model_dir}/median_values.joblib")

        X = df[self.num_cols + self.cat_cols]
        return X, y

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not hasattr(self, 'encoders') or not hasattr(self, 'median_values'):
            if not self.load_encoders():
                raise RuntimeError("Encoders not loaded and not found on disk.")

        for col in self.num_cols:
            if col not in df.columns:
                df[col] = self.median_values.get(col, 0)
        df[self.num_cols] = df[self.num_cols].fillna(value=self.median_values)

        for col in self.cat_cols:
            if col not in df.columns:
                df[col] = 'UNKNOWN'
            df[col] = df[col].fillna('UNKNOWN').astype(str).str.upper()
            
            if col in self.encoders:
                cat_type = pd.CategoricalDtype(categories=list(self.encoders[col].values()))
                df[col] = df[col].astype(cat_type)

        return df[self.num_cols + self.cat_cols]

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features.
        """
        df_copy = df.copy()
        current_year = datetime.datetime.now().year
        
        # Calculate age
        if 'registration_year' in df_copy.columns:
            df_copy['age'] = current_year - df_copy['registration_year']
        else:
            df_copy['age'] = 5 # default fallback
            
        # Calculate km per year
        if 'km_driven' in df_copy.columns:
            df_copy['km_per_year'] = df_copy['km_driven'] / df_copy['age'].replace(0, 1)
        else:
            df_copy['km_per_year'] = 10000
            
        # Add seasonality indicator (month of posting)
        if 'first_seen' in df_copy.columns:
            df_copy['season_month'] = pd.to_datetime(df_copy['first_seen']).dt.month
        else:
            df_copy['season_month'] = datetime.datetime.now().month
            
        # Supply/demand indicator mock feature (since we don't have full supply index in real-time context)
        df_copy['supply_index'] = np.random.uniform(0.8, 1.2, len(df_copy))
        
        if 'age' not in self.num_cols:
            self.num_cols.extend(['age', 'km_per_year', 'season_month', 'supply_index'])
            
        return df_copy
