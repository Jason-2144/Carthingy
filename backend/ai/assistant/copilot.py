from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import google.generativeai as genai
import os
import json
from backend.search.engine import search_engine
from backend.deal_engine.scorer import deal_scorer

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

class AICopilot:
    async def chat(self, user_query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Translates user query into a search context, fetches data from our DB/Search Engine,
        and returns a natural language response with actual data.
        """
        # Step 1: Use LLM to extract structured search parameters
        prompt = f"""
        You are an AI assistant for a used car platform. Extract search parameters from the user's query.
        Return ONLY valid JSON with keys: 'query' (text), 'price_max' (int), 'price_min' (int), 
        'make' (string or list), 'model' (string), 'city' (string), 'body_type' (string).
        If a field is not present, omit it. Do not use markdown blocks.
        
        User Query: "{user_query}"
        """
        
        try:
            response = model.generate_content(prompt)
            # Clean JSON
            json_str = response.text.strip().replace('```json', '').replace('```', '')
            search_params = json.loads(json_str)
        except Exception as e:
            search_params = {"query": user_query}
            
        # Extract filters
        filters = {}
        if "price_max" in search_params: filters["price_max"] = search_params["price_max"]
        if "price_min" in search_params: filters["price_min"] = search_params["price_min"]
        if "make" in search_params: filters["make"] = search_params["make"]
        if "city" in search_params: filters["registration_city"] = search_params["city"]
        if "body_type" in search_params: filters["body_type"] = search_params["body_type"]
        
        q = search_params.get("query", "")
        if "make" in search_params and "model" in search_params:
            q = f"{search_params['make']} {search_params['model']}"
            
        # Step 2: Query our Search Engine
        results = await search_engine.search_listings(query=q, filters=filters, limit=5, sort_by="deal_score")
        
        # Step 3: Use LLM to formulate a response based on REAL data
        hits = results.get("hits", [])
        if not hits:
            return {
                "message": "I couldn't find any exact matches for your criteria in our current inventory. Would you like me to set up an alert for this?",
                "data": []
            }
            
        cars_summary = []
        for i, hit in enumerate(hits):
            cars_summary.append(f"{i+1}. {hit.get('title')} ({hit.get('registration_year')}) - ₹{hit.get('price')} in {hit.get('registration_city')}. Deal Score: {hit.get('deal_score', 'N/A')}/100")
            
        summary_str = "\n".join(cars_summary)
        
        synthesis_prompt = f"""
        User Query: "{user_query}"
        Here are the top cars from our database that match:
        {summary_str}
        
        Write a helpful, concise response to the user summarizing these options. Highlight the best deal if applicable.
        """
        
        try:
            final_response = model.generate_content(synthesis_prompt)
            message = final_response.text
        except Exception:
            message = f"I found {len(hits)} cars that match your search. The best matches are listed below."
            
        return {
            "message": message,
            "data": hits,
            "filters_applied": filters
        }

copilot = AICopilot()
