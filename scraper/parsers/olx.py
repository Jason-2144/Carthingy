from scraper.normalizers.car import CarNormalizer
import json

class OLXParser:
    """
    Takes the raw dictionary extracted by OLXConnector and transforms it 
    into a structured schema that matches the database models.
    """
    def parse(self, raw_data: dict) -> dict:
        if "error" in raw_data:
            return raw_data

        attributes = raw_data.get("attributes", [])
        
        # OLX attributes are usually paired like: ["Brand", "Maruti Suzuki", "Model", "Swift", "Year", "2015"]
        # Convert to dictionary for easier access
        attr_dict = {}
        for i in range(0, len(attributes) - 1, 2):
            key = attributes[i].strip().lower()
            val = attributes[i+1].strip()
            attr_dict[key] = val

        parsed = {
            "external_listing_id": self._extract_id_from_url(raw_data.get("url", "")),
            "url": raw_data.get("url"),
            "marketplace": raw_data.get("marketplace"),
            "title": raw_data.get("title", ""),
            "description": raw_data.get("description", ""),
            "price": CarNormalizer.normalize_price(raw_data.get("price")),
            "images": raw_data.get("images", []),
            "seller_name": raw_data.get("seller_name", "Unknown"),
            
            # Mapped attributes
            "make": attr_dict.get("brand"),
            "model": attr_dict.get("model"),
            "registration_year": CarNormalizer.normalize_year(attr_dict.get("year", attr_dict.get("registration year"))),
            "km_driven": CarNormalizer.normalize_mileage(attr_dict.get("km driven")),
            "fuel": CarNormalizer.normalize_fuel(attr_dict.get("fuel")),
            "transmission": CarNormalizer.normalize_transmission(attr_dict.get("transmission")),
            "ownership": CarNormalizer.normalize_ownership(attr_dict.get("no. of owners")),
            
            # Location is often in a specific div on OLX, if missing, default or extract from URL
            "registration_state": "Unknown",
            "registration_city": "Unknown",
            "colour": attr_dict.get("color"),
        }
        
        # Basic validation
        if not parsed["price"] or not parsed["title"]:
            parsed["error"] = "Missing essential fields (price or title)"

        return parsed

    def _extract_id_from_url(self, url: str) -> str:
        # OLX URLs usually end with iid-<ID>
        if "iid-" in url:
            return url.split("iid-")[-1].split("?")[0]
        # Fallback to hash
        return str(hash(url))
