from backend.search.indexes.client import search_client
from backend.search.config import search_settings
from typing import List

class RankingManager:
    def update_ranking_rules(self, custom_rules: List[str] = None):
        """
        Updates the ranking rules in Meilisearch. 
        Higher order in the list = higher priority.
        """
        default_rules = [
            "words",
            "typo",
            "proximity",
            "attribute",
            "sort",
            "exactness",
            "deal_score:desc",
            "first_seen:desc"
        ]
        rules = custom_rules if custom_rules else default_rules
        search_client.update_settings(
            search_settings.LISTINGS_INDEX,
            {"rankingRules": rules}
        )

ranking_manager = RankingManager()
