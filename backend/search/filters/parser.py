import re
from typing import Dict, Any, Tuple

class NaturalQueryParser:
    def __init__(self):
        # A simple keyword-based parser for demonstration.
        # In a real enterprise system, you could use an LLM or SpaCy here.
        self.makes = ["toyota", "honda", "maruti suzuki", "hyundai", "tata", "mahindra", "kia", "mg", "volkswagen", "skoda", "bmw", "mercedes-benz", "audi"]
        self.body_types = ["suv", "sedan", "hatchback", "muv", "luxury"]
        self.fuels = ["petrol", "diesel", "cng", "electric"]
        self.transmissions = ["automatic", "manual"]
        
    def parse(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parses a natural language query into a base text query and structured filters.
        e.g., "Toyota SUV under 8 lakh automatic" -> 
        Text: "Toyota", Filters: {body_type: SUV, price: {max: 800000}, transmission: automatic}
        """
        original_query = query
        q_lower = query.lower()
        filters = {}
        
        # 1. Price extraction: "under 8 lakh", "less than 20 lakhs", "below 500000"
        price_match = re.search(r'(under|less than|below)\s+(\d+(?:\.\d+)?)\s*(lakh|l|k|)?', q_lower)
        if price_match:
            val = float(price_match.group(2))
            unit = price_match.group(3)
            if unit in ["lakh", "l"]:
                val *= 100000
            elif unit == "k":
                val *= 1000
            filters["price_max"] = int(val)
            # Remove from query text so it doesn't mess up text search
            query = re.sub(price_match.group(0), '', query, flags=re.IGNORECASE)
            
        # 2. Mileage extraction: "under 50,000 km", "less than 50k km"
        km_match = re.search(r'(under|less than|below)\s+(\d+(?:,\d+)?)\s*(k|km|kms)?', q_lower)
        if km_match:
            # check if it overlaps with price. if 'km' in group 3, it's km
            unit = km_match.group(3)
            if unit in ["km", "kms"] or (not price_match and unit == "k"):
                val_str = km_match.group(2).replace(',', '')
                val = int(val_str)
                if unit == "k":
                    val *= 1000
                filters["km_driven_max"] = val
                query = re.sub(km_match.group(0), '', query, flags=re.IGNORECASE)
                
        # 3. Year/Age extraction: "less than 5 years old", "post 2018"
        age_match = re.search(r'(under|less than|below)\s+(\d+)\s*(years|yrs)', q_lower)
        if age_match:
            val = int(age_match.group(2))
            import datetime
            min_year = datetime.datetime.now().year - val
            filters["registration_year_min"] = min_year
            query = re.sub(age_match.group(0), '', query, flags=re.IGNORECASE)
            
        # 4. Attributes extraction
        for bt in self.body_types:
            if bt in q_lower:
                filters["body_type"] = bt.title()
                query = re.sub(r'\b' + bt + r'\b', '', query, flags=re.IGNORECASE)
                
        for f in self.fuels:
            if f in q_lower:
                filters["fuel"] = f.title()
                query = re.sub(r'\b' + f + r'\b', '', query, flags=re.IGNORECASE)
                
        for t in self.transmissions:
            if t in q_lower:
                filters["transmission"] = t.title()
                query = re.sub(r'\b' + t + r'\b', '', query, flags=re.IGNORECASE)

        # Return the cleaned text query and the extracted filters
        return query.strip(), filters

nl_parser = NaturalQueryParser()
