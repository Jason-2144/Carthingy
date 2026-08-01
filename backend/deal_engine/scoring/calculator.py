import datetime
from backend.deal_engine.config import deal_settings

class DealScoreCalculator:
    def calculate_score(self, listing_data: dict, market_stats: dict, estimated_value: float) -> float:
        """
        Calculates a deal score from 0 to 100 based on weighted factors.
        """
        score = 0.0
        
        # 1. Valuation Difference Score
        price = listing_data.get('price', 0)
        if estimated_value > 0 and price > 0:
            diff_pct = (estimated_value - price) / estimated_value
            # +20% or more under market = 100 points
            # -20% or more over market = 0 points
            val_score = max(0, min(100, (diff_pct + 0.20) / 0.40 * 100))
            score += val_score * deal_settings.WEIGHT_VALUATION_DIFF
            
        # 2. Mileage Score
        km_driven = listing_data.get('km_driven', 0)
        avg_km = market_stats.get('avg_km', 50000)
        if avg_km > 0:
            km_ratio = km_driven / avg_km
            km_score = max(0, min(100, (2.0 - km_ratio) * 50))
            score += km_score * deal_settings.WEIGHT_MILEAGE
            
        # 3. Age Score
        current_year = datetime.datetime.now().year
        age = current_year - listing_data.get('registration_year', current_year)
        avg_age = market_stats.get('avg_age', 5)
        if avg_age > 0:
            age_ratio = age / avg_age
            age_score = max(0, min(100, (2.0 - age_ratio) * 50))
            score += age_score * deal_settings.WEIGHT_AGE
            
        # 4. Ownership Score
        ownership = listing_data.get('ownership', 1)
        # 1st owner = 100, 2nd = 75, 3rd = 40, 4th+ = 0
        own_score = max(0, 100 - ((ownership - 1) * 30))
        score += own_score * deal_settings.WEIGHT_OWNERSHIP
        
        # 5. Days on Market Score
        dom = listing_data.get('days_on_market', 0)
        # Fresh (0) = 100, Old (90+) = 0
        dom_score = max(0, min(100, 100 - (dom / 90 * 100)))
        score += dom_score * deal_settings.WEIGHT_DAYS_ON_MARKET
        
        # 6. Demand Score
        demand_score = market_stats.get('demand_score', 50)
        score += demand_score * deal_settings.WEIGHT_DEMAND
        
        # 7. Price Drops Score
        price_drops = listing_data.get('price_drop_count', 0)
        # More drops = slightly better score as seller is motivated, up to a point
        drop_score = min(100, price_drops * 25)
        score += drop_score * deal_settings.WEIGHT_PRICE_DROPS
        
        # 8. Seller Reliability
        seller_score = market_stats.get('seller_reliability', 80)
        score += seller_score * deal_settings.WEIGHT_SELLER_RELIABILITY
        
        return round(score, 2)

score_calculator = DealScoreCalculator()
