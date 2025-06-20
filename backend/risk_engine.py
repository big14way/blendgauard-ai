import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

class LiquidationPredictor:
    def __init__(self, model_path='model.pkl'):
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            self.model = self._train_mock_model()
            joblib.dump(self.model, model_path)
    
    def _train_mock_model(self):
        X, y = make_classification(n_samples=1000, n_features=4, random_state=42)
        model = RandomForestClassifier()
        model.fit(X, y)
        return model
    
    def predict(self, position_data: dict) -> float:
        # Expected features: ltv, asset_volatility, pool_utilization, trend
        features = [position_data[k] for k in ['ltv', 'asset_volatility', 'pool_utilization', 'trend']]
        return self.model.predict_proba([features])[0][1] 