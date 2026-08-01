import pytest
import datetime
from backend.deal_engine.scoring.calculator import score_calculator
from backend.deal_engine.recommendations.classifier import deal_classifier
from backend.deal_engine.pricing.negotiation import negotiation_engine
from backend.deal_engine.pricing.dealer import dealer_profit_calculator

def test_score_calculator():
    listing_data = {
        "price": 450000,
        "km_driven": 30000,
        "registration_year": 2020,
        "ownership": 1,
        "days_on_market": 5,
        "price_drop_count": 0
    }
    market_stats = {
        "avg_km": 50000,
        "avg_age": 5,
        "demand_score": 80,
        "seller_reliability": 90
    }
    estimated_value = 500000
    
    score = score_calculator.calculate_score(listing_data, market_stats, estimated_value)
    
    # 450k vs 500k = 10% under market. Should be a high score.
    assert score > 0
    assert score <= 100
    
    # Check if a severely overpriced car gets a lower score
    listing_data_overpriced = listing_data.copy()
    listing_data_overpriced["price"] = 700000
    score_overpriced = score_calculator.calculate_score(listing_data_overpriced, market_stats, estimated_value)
    assert score_overpriced < score

def test_deal_classifier():
    assert deal_classifier.classify(95) == "Exceptional Deal"
    assert deal_classifier.classify(85) == "Excellent Deal"
    assert deal_classifier.classify(75) == "Good Deal"
    assert deal_classifier.classify(55) == "Fair Price"
    assert deal_classifier.classify(45) == "Slightly Overpriced"
    assert deal_classifier.classify(25) == "Overpriced"
    assert deal_classifier.classify(10) == "Avoid"

def test_negotiation_engine():
    # Fairly priced
    result = negotiation_engine.estimate_negotiation(price=500000, estimated_value=500000, deal_score=50, days_on_market=10)
    assert result["negotiation_margin_pct"] >= 5.0
    
    # Overpriced + old listing
    result_over = negotiation_engine.estimate_negotiation(price=600000, estimated_value=500000, deal_score=20, days_on_market=80)
    assert result_over["negotiation_margin_pct"] > result["negotiation_margin_pct"]

def test_dealer_profit_calculator():
    purchase_price = 400000
    estimated_retail = 500000
    
    result = dealer_profit_calculator.calculate(purchase_price, estimated_retail)
    
    assert "expected_gross_profit" in result
    assert "expected_roi_pct" in result
    assert "break_even_purchase_price" in result
    
    # Gross profit = 500k - (400k + recon + trans + reg)
    assert result["expected_gross_profit"] < (estimated_retail - purchase_price)

