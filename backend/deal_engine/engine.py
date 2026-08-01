from backend.deal_engine.scoring.calculator import score_calculator
from backend.deal_engine.recommendations.classifier import deal_classifier
from backend.deal_engine.pricing.negotiation import negotiation_engine
from backend.deal_engine.pricing.dealer import dealer_profit_calculator
from backend.deal_engine.analytics.market_demand import market_demand_engine
from backend.deal_engine.ranking.similarity import similarity_engine
import datetime

class DealIntelligenceEngine:
    async def analyze_listing(self, listing_data: dict, estimated_market_value: float) -> dict:
        """
        The main entrypoint for the Deal Intelligence Engine.
        Analyzes a single listing and returns a comprehensive deal report.
        """
        price = float(listing_data.get('price', 0))
        make = listing_data.get('make', 'Unknown')
        model = listing_data.get('model', 'Unknown')
        city = listing_data.get('registration_city', 'Unknown')
        
        # Calculate days on market
        first_seen = listing_data.get('first_seen')
        if first_seen:
            if isinstance(first_seen, str):
                first_seen = datetime.datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
            # naive subtraction if timezone naive, assuming aware for now
            try:
                dom = (datetime.datetime.now(datetime.timezone.utc) - first_seen).days
            except TypeError:
                dom = (datetime.datetime.now() - first_seen).days
        else:
            dom = 0
            
        listing_data['days_on_market'] = max(0, dom)

        # 1. Market Stats
        market_stats = await market_demand_engine.get_demand_metrics(make, model, city)
        
        # 2. Deal Score
        score = score_calculator.calculate_score(listing_data, market_stats, estimated_market_value)
        
        # 3. Recommendation
        classification = deal_classifier.classify(score)
        explanation = deal_classifier.explain(classification, score)
        
        # 4. Negotiation Estimate
        negotiation = negotiation_engine.estimate_negotiation(
            price, estimated_market_value, score, listing_data['days_on_market']
        )
        
        # 5. Dealer Profit
        profit = dealer_profit_calculator.calculate(price, estimated_market_value)
        
        return {
            "deal_score": score,
            "recommendation": {
                "classification": classification,
                "explanation": explanation
            },
            "market_demand": market_stats,
            "negotiation": negotiation,
            "dealer_profit": profit
        }
        
    async def get_similar_vehicles(self, listing_id: str, limit: int = 20) -> list:
        return await similarity_engine.find_similar(listing_id, limit)

deal_engine = DealIntelligenceEngine()
