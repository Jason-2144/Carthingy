from backend.search.indexes.client import search_client
from backend.search.config import search_settings
from typing import Dict, List

class SynonymManager:
    def get_synonyms(self) -> Dict[str, List[str]]:
        return {
            "suv": ["sports utility vehicle", "jeep", "4x4"],
            "maruti": ["maruti suzuki", "suzuki"],
            "bmw": ["bayerische motoren werke", "bimmer"],
            "mercedes": ["mercedes-benz", "merc", "benz"],
            "vw": ["volkswagen"],
            "automatic": ["amt", "cvt", "dsg", "dct", "torque converter"],
            "petrol": ["gasoline"],
            "diesel": ["crdi", "tdci", "ddis"]
        }
        
    def apply_synonyms(self):
        synonyms = self.get_synonyms()
        settings = {
            "synonyms": synonyms
        }
        search_client.update_settings(search_settings.LISTINGS_INDEX, settings)

synonym_manager = SynonymManager()
