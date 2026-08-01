from scraper.normalizers.car import CarNormalizer
import re

class FacebookParser:
    def parse(self, raw_data: dict) -> dict:
        if "error" in raw_data:
            return raw_data

        attributes = raw_data.get("attributes", [])
        
        # Facebook lists attributes as string blocks, e.g., "Driven 15,000 km", "Automatic transmission", "Exterior color: Black"
        parsed = {
            "external_listing_id": self._extract_id_from_url(raw_data.get("url", "")),
            "url": raw_data.get("url"),
            "marketplace": raw_data.get("marketplace"),
            "title": raw_data.get("title", ""),
            "description": raw_data.get("description", ""),
            "price": CarNormalizer.normalize_price(raw_data.get("price")),
            "images": raw_data.get("images", []),
            "seller_name": "Facebook User", # Often requires deeper scraping
            
            "make": None,
            "model": None,
            "registration_year": CarNormalizer.normalize_year(raw_data.get("title", "")), # Often in title
            "km_driven": None,
            "fuel": None,
            "transmission": None,
            "ownership": 1,
            "registration_state": "Unknown",
            "registration_city": "Unknown",
            "colour": None,
        }

        # Attempt to parse attributes from strings
        for attr in attributes:
            attr_lower = attr.lower()
            if "driven" in attr_lower and "km" in attr_lower:
                parsed["km_driven"] = CarNormalizer.normalize_mileage(attr)
            if "transmission" in attr_lower:
                parsed["transmission"] = CarNormalizer.normalize_transmission(attr)
            if "exterior" in attr_lower:
                parsed["colour"] = attr.split(":")[-1].strip()
            if "fuel type" in attr_lower:
                parsed["fuel"] = CarNormalizer.normalize_fuel(attr)

        # Basic title parsing for Make/Model (Fallback)
        title_parts = parsed["title"].split(" ")
        if len(title_parts) >= 2 and not parsed["make"]:
            # Year is often first part
            if re.match(r'^\d{4}$', title_parts[0]):
                parsed["make"] = title_parts[1]
                if len(title_parts) > 2:
                    parsed["model"] = title_parts[2]
            else:
                parsed["make"] = title_parts[0]
                parsed["model"] = title_parts[1]

        return parsed

    def _extract_id_from_url(self, url: str) -> str:
        # FB marketplace item urls look like: /marketplace/item/123456789/
        match = re.search(r'/item/(\d+)', url)
        if match:
            return match.group(1)
        return str(hash(url))
