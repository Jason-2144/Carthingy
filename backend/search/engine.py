from typing import Dict, Any, List, Optional
from backend.search.indexes.client import search_client
from backend.search.autocomplete.suggester import suggester
from backend.search.filters.parser import nl_parser
from backend.search.analytics.tracker import search_analytics
from backend.search.config import search_settings
import time

class SearchEngine:
    def build_meili_filter(self, structured_filters: Dict[str, Any]) -> List[str]:
        filter_strs = []
        for key, value in structured_filters.items():
            if value is None:
                continue
                
            if key == "price_min":
                filter_strs.append(f"price >= {value}")
            elif key == "price_max":
                filter_strs.append(f"price <= {value}")
            elif key == "km_driven_min":
                filter_strs.append(f"km_driven >= {value}")
            elif key == "km_driven_max":
                filter_strs.append(f"km_driven <= {value}")
            elif key == "registration_year_min":
                filter_strs.append(f"registration_year >= {value}")
            elif key == "registration_year_max":
                filter_strs.append(f"registration_year <= {value}")
            elif key == "deal_score_min":
                filter_strs.append(f"deal_score >= {value}")
            elif isinstance(value, list) and len(value) > 0:
                conds = [f"{key} = '{v}'" for v in value]
                filter_strs.append("(" + " OR ".join(conds) + ")")
            elif isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
                filter_strs.append(f"{key} = '{value}'")
                
        return filter_strs

    async def search_listings(
        self, 
        query: str = "", 
        filters: Dict[str, Any] = None, 
        sort_by: str = None, 
        page: int = 1, 
        limit: int = search_settings.DEFAULT_PAGE_SIZE,
        user_id: str = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        if filters is None:
            filters = {}

        if search_settings.ENABLE_NLP_PARSING and query:
            clean_query, nl_filters = nl_parser.parse(query)
            query = clean_query
            for k, v in nl_filters.items():
                if k not in filters:
                    filters[k] = v
                    
        meili_filters = self.build_meili_filter(filters)
        
        search_params = {
            "offset": (page - 1) * limit,
            "limit": limit,
            "filter": meili_filters,
        }
        
        if sort_by:
            if sort_by == "price_asc":
                search_params["sort"] = ["price:asc"]
            elif sort_by == "price_desc":
                search_params["sort"] = ["price:desc"]
            elif sort_by == "newest":
                search_params["sort"] = ["first_seen:desc"]
            elif sort_by == "deal_score":
                search_params["sort"] = ["deal_score:desc"]
            elif sort_by == "km_asc":
                search_params["sort"] = ["km_driven:asc"]
                
        results = search_client.search(search_settings.LISTINGS_INDEX, query, **search_params)
        
        latency = (time.time() - start_time) * 1000
        
        await search_analytics.log_search(
            user_id=user_id,
            query=query,
            filters=filters,
            results_count=results.get("estimatedTotalHits", len(results.get("hits", []))),
            latency_ms=latency
        )
        
        return {
            "hits": results.get("hits", []),
            "estimatedTotalHits": results.get("estimatedTotalHits", 0),
            "processingTimeMs": results.get("processingTimeMs", 0),
            "applied_filters": filters,
            "clean_query": query
        }

    async def get_autocomplete_suggestions(self, query: str) -> List[str]:
        return await suggester.get_suggestions(query)

search_engine = SearchEngine()
