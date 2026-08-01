from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class BaseValuationModel(ABC):
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: str) -> 'BaseValuationModel':
        pass
