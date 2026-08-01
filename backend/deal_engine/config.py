from pydantic_settings import BaseSettings

class DealEngineSettings(BaseSettings):
    # Deal Score Weights
    WEIGHT_VALUATION_DIFF: float = 0.40
    WEIGHT_MILEAGE: float = 0.15
    WEIGHT_AGE: float = 0.10
    WEIGHT_OWNERSHIP: float = 0.05
    WEIGHT_DAYS_ON_MARKET: float = 0.10
    WEIGHT_DEMAND: float = 0.10
    WEIGHT_PRICE_DROPS: float = 0.05
    WEIGHT_SELLER_RELIABILITY: float = 0.05
    
    # Negotiation Factors
    NEGOTIATION_BASE_MARGIN: float = 0.05  # Base 5% negotiation room
    NEGOTIATION_MAX_MARGIN: float = 0.15   # Max 15% room for overpriced/old listings
    
    # Dealer Profit Defaults
    RECONDITIONING_COST_BASE: float = 15000.0  # INR
    TRANSPORT_COST_BASE: float = 5000.0        # INR
    REGISTRATION_COST_BASE: float = 2000.0     # INR
    DEALER_TARGET_MARGIN: float = 0.10         # 10% target margin
    
    # Score Thresholds for Recommendations
    SCORE_EXCEPTIONAL: float = 90.0
    SCORE_EXCELLENT: float = 80.0
    SCORE_GOOD: float = 70.0
    SCORE_FAIR: float = 50.0
    SCORE_SLIGHTLY_OVERPRICED: float = 40.0
    SCORE_OVERPRICED: float = 20.0
    
    class Config:
        env_prefix = "DEAL_"

deal_settings = DealEngineSettings()
