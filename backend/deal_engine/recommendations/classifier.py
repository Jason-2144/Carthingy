from backend.deal_engine.config import deal_settings

class DealClassifier:
    def classify(self, score: float) -> str:
        if score >= deal_settings.SCORE_EXCEPTIONAL:
            return "Exceptional Deal"
        elif score >= deal_settings.SCORE_EXCELLENT:
            return "Excellent Deal"
        elif score >= deal_settings.SCORE_GOOD:
            return "Good Deal"
        elif score >= deal_settings.SCORE_FAIR:
            return "Fair Price"
        elif score >= deal_settings.SCORE_SLIGHTLY_OVERPRICED:
            return "Slightly Overpriced"
        elif score >= deal_settings.SCORE_OVERPRICED:
            return "Overpriced"
        else:
            return "Avoid"

    def explain(self, classification: str, score: float) -> str:
        explanations = {
            "Exceptional Deal": "This vehicle is priced significantly below market value and has excellent attributes. Buy immediately.",
            "Excellent Deal": "Highly attractive pricing combined with solid vehicle history and condition.",
            "Good Deal": "A solid purchase. Priced competitively with acceptable wear and history.",
            "Fair Price": "Priced accurately according to current market conditions.",
            "Slightly Overpriced": "Asking price is higher than market average. Negotiation is recommended.",
            "Overpriced": "Significantly overpriced for its condition and market value. Strong negotiation required.",
            "Avoid": "Not recommended due to severe overpricing or poor vehicle attributes."
        }
        return explanations.get(classification, "No explanation available.")

deal_classifier = DealClassifier()
