import json
import datetime
from backend.valuation.statistics.market import market_intelligence_service

class ReportGenerator:
    async def generate_monthly_report(self) -> dict:
        fastest_selling = await market_intelligence_service.get_fastest_selling_models()
        trends = await market_intelligence_service.get_price_trends()
        
        report = {
            "generated_at": datetime.datetime.now().isoformat(),
            "fastest_selling_models": fastest_selling,
            "price_trends_by_body_type": trends
        }
        
        # In a real system, save to S3 or DB, here we just return the dict
        return report

report_generator = ReportGenerator()
