import pytest
import pandas as pd
import numpy as np
from backend.valuation.features.extractor import FeatureExtractor
from backend.valuation.models.lgbm_model import LightGBMValuationModel
from backend.valuation.prediction.service import PredictionService

def test_feature_extractor():
    extractor = FeatureExtractor(model_dir="/tmp/test_models")
    df = pd.DataFrame([
        {
            "price": 500000, "make": "Honda", "model": "City", "variant": "V",
            "fuel": "Petrol", "transmission": "Manual", "body_type": "Sedan",
            "registration_year": 2018, "km_driven": 45000, "ownership": 1,
            "registration_city": "Delhi", "registration_state": "Delhi"
        }
    ])
    
    df_ext = extractor.extract_features(df)
    assert 'age' in df_ext.columns
    assert 'km_per_year' in df_ext.columns
    
    X, y = extractor.fit_transform(df_ext)
    assert len(X) == 1
    assert y is not None
    assert np.isclose(y[0], np.log1p(500000))

def test_model_training():
    model = LightGBMValuationModel(num_boost_round=10)
    X_train = pd.DataFrame({"feat1": [1, 2, 3], "feat2": [4, 5, 6]})
    y_train = pd.Series([10, 20, 30])
    
    model.train(X_train, y_train)
    preds = model.predict(X_train)
    
    assert len(preds) == 3
    assert all(isinstance(p, float) for p in preds)
