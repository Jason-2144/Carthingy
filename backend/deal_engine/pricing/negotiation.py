from backend.deal_engine.config import deal_settings

class NegotiationEngine:
    def estimate_negotiation(self, price: float, estimated_value: float, deal_score: float, days_on_market: int) -> dict:
        """
        Estimates how much a buyer can negotiate.
        """
        if price <= 0:
            return {}

        # Base margin
        margin_pct = deal_settings.NEGOTIATION_BASE_MARGIN
        
        # If overpriced, more room to negotiate
        if price > estimated_value:
            overprice_pct = (price - estimated_value) / estimated_value
            margin_pct += min(overprice_pct, 0.10) # Add up to 10% more
            
        # If on market for a long time (e.g. > 60 days), add more room
        if days_on_market > 60:
            margin_pct += 0.02
            
        # Cap the margin
        margin_pct = min(margin_pct, deal_settings.NEGOTIATION_MAX_MARGIN)
        
        # If it's a steal, less room
        if deal_score >= deal_settings.SCORE_EXCELLENT:
            margin_pct = max(0.01, margin_pct - 0.03)

        suggested_offer = price * (1 - margin_pct)
        savings = price - suggested_offer
        
        # Acceptance range
        min_accept = suggested_offer * 0.98
        max_accept = suggested_offer * 1.02
        
        # Probability based on score and time
        prob = 50 + (days_on_market / 90 * 30) - (deal_score / 100 * 20)
        prob = max(10, min(95, prob))
        
        return {
            "suggested_offer_price": round(suggested_offer, 2),
            "likely_acceptance_range": {
                "min": round(min_accept, 2),
                "max": round(max_accept, 2)
            },
            "negotiation_margin_pct": round(margin_pct * 100, 2),
            "estimated_savings": round(savings, 2),
            "probability_of_success_pct": round(prob, 1)
        }

negotiation_engine = NegotiationEngine()
