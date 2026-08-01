import lightgbm as lgb
import numpy as np
import pandas as pd
import joblib
from .base_model import BaseValuationModel

class LightGBMValuationModel(BaseValuationModel):
    def __init__(self, **params):
        self.model = None
        self.params = params or {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'learning_rate': 0.05,
            'num_leaves': 63,
            'max_depth': 8,
            'feature_fraction': 0.8,
            'verbose': -1,
            'random_state': 42
        }

    def train(self, X: pd.DataFrame, y: pd.Series, X_val: pd.DataFrame = None, y_val: pd.Series = None, **kwargs):
        train_data = lgb.Dataset(X, label=y)
        valid_sets = [train_data]
        if X_val is not None and y_val is not None:
            val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
            valid_sets.append(val_data)
            
        num_boost_round = kwargs.get('num_boost_round', 1000)
        early_stopping_rounds = kwargs.get('early_stopping_rounds', 50)
        
        callbacks = []
        if early_stopping_rounds and X_val is not None:
            callbacks.append(lgb.early_stopping(stopping_rounds=early_stopping_rounds, verbose=False))
            
        self.model = lgb.train(
            self.params,
            train_data,
            valid_sets=valid_sets,
            num_boost_round=num_boost_round,
            callbacks=callbacks
        )

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained or loaded.")
        # Return exact prediction (remember it's log1p transformed, so we need expm1 later)
        return self.model.predict(X)

    def feature_importance(self) -> dict:
        if self.model is None:
            return {}
        importance = self.model.feature_importance(importance_type='gain')
        features = self.model.feature_name()
        return dict(zip(features, importance))

    def save(self, path: str):
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> 'LightGBMValuationModel':
        instance = cls()
        instance.model = joblib.load(path)
        return instance
