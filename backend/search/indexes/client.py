import meilisearch
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from backend.search.config import search_settings

class SearchClientInterface(ABC):
    @abstractmethod
    def add_documents(self, index_name: str, documents: List[Dict[str, Any]]):
        pass

    @abstractmethod
    def search(self, index_name: str, query: str, **kwargs) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def update_settings(self, index_name: str, settings: Dict[str, Any]):
        pass

    @abstractmethod
    def delete_document(self, index_name: str, doc_id: str):
        pass

class MeiliSearchClient(SearchClientInterface):
    def __init__(self):
        self.client = meilisearch.Client(search_settings.MEILI_URL, search_settings.MEILI_MASTER_KEY)

    def add_documents(self, index_name: str, documents: List[Dict[str, Any]]):
        if not documents:
            return
        index = self.client.index(index_name)
        return index.add_documents(documents)

    def search(self, index_name: str, query: str, **kwargs) -> Dict[str, Any]:
        index = self.client.index(index_name)
        return index.search(query, kwargs)
        
    def update_settings(self, index_name: str, settings: Dict[str, Any]):
        index = self.client.index(index_name)
        return index.update_settings(settings)
        
    def delete_document(self, index_name: str, doc_id: str):
        index = self.client.index(index_name)
        return index.delete_document(doc_id)

    def setup_listings_index(self):
        settings = {
            "searchableAttributes": [
                "title", "make", "model", "variant", "registration_city", "registration_state", "colour", "fuel", "transmission", "body_type"
            ],
            "filterableAttributes": [
                "price", "registration_year", "km_driven", "ownership", 
                "make", "model", "variant", "fuel", "transmission", 
                "registration_city", "registration_state", "status",
                "body_type", "seller_type", "deal_score", "market_value",
                "days_on_market"
            ],
            "sortableAttributes": [
                "price", "registration_year", "km_driven", "deal_score", "market_value", "first_seen", "price_drop_count"
            ],
            "rankingRules": [
                "words",
                "typo",
                "proximity",
                "attribute",
                "sort",
                "exactness",
                "deal_score:desc",
                "first_seen:desc"
            ]
        }
        self.update_settings(search_settings.LISTINGS_INDEX, settings)

search_client = MeiliSearchClient()
