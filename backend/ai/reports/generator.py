import json
import google.generativeai as genai
import os
from typing import Dict, Any, List

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

class AIReportGenerator:
    async def generate_market_report(self, city: str, make: str, model_name: str, data: List[Dict[str, Any]]) -> str:
        """
        Generates an executive market summary based on real database metrics.
        """
        if not data:
            return f"Insufficient data to generate a market report for {make} {model_name} in {city}."
            
        avg_price = sum([d.get('price', 0) for d in data]) / len(data)
        count = len(data)
        
        prompt = f"""
        You are an expert automotive market analyst. Generate a brief Executive Market Report.
        
        Market Context:
        - Location: {city}
        - Vehicle: {make} {model_name}
        - Active Listings: {count}
        - Average Price: ₹{avg_price:,.2f}
        
        Write a professional summary discussing the demand, pricing trends, and whether this is a buyer's or seller's market based on this limited data.
        Keep it to 3 paragraphs max. Use markdown formatting.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Failed to generate report: {str(e)}"

ai_report_generator = AIReportGenerator()
