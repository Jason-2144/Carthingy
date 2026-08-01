from backend.search.indexes.client import search_client
from backend.search.analytics.tracker import search_analytics
from backend.search.config import search_settings
from typing import List

class AutocompleteSuggester:
    async def get_suggestions(self, query: str) -> List[str]:
        if not query:
            # Return trending/popular searches if query is empty
            return await search_analytics.get_popular_queries(limit=5)
            
        # We can query Meilisearch for exact completions
        results = search_client.search(
            search_settings.LISTINGS_INDEX, 
            query, 
            limit=5, 
            attributesToRetrieve=["make", "model", "variant", "registration_city"]
        )
        
        suggestions = []
        for hit in results.get("hits", []):
            make = hit.get("make")
            model = hit.get("model")
            
            # Form suggestion string
            sugg = f"{make} {model}"
            if sugg not in suggestions:
                suggestions.append(sugg)
                
        # Also mix in popular queries that match
        popular = await search_analytics.get_popular_queries(limit=20)
        for p in popular:
            if query.lower() in p.lower() and p not in suggestions:
                suggestions.append(p)
                
        return suggestions[:10]

suggester = AutocompleteSuggester()
