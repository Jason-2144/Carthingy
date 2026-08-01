import re
from typing import Any

class CarNormalizer:
    """
    Cleans and standardizes raw text extracted from marketplaces.
    """
    
    @staticmethod
    def normalize_price(price_str: str | None) -> float | None:
        if not price_str:
            return None
        # Remove currency symbols and commas
        clean_str = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(clean_str)
        except ValueError:
            return None

    @staticmethod
    def normalize_mileage(km_str: str | None) -> int | None:
        if not km_str:
            return None
        # Sometimes it says "15,000 km" or "15k"
        km_str = km_str.lower()
        multiplier = 1
        if 'k' in km_str and 'km' not in km_str:
            multiplier = 1000
        
        clean_str = re.sub(r'[^\d]', '', km_str)
        try:
            return int(clean_str) * multiplier
        except ValueError:
            return None

    @staticmethod
    def normalize_year(year_str: str | None) -> int | None:
        if not year_str:
            return None
        # Find 4 digits
        match = re.search(r'(19|20)\d{2}', year_str)
        if match:
            return int(match.group(0))
        return None

    @staticmethod
    def normalize_ownership(own_str: str | None) -> int:
        if not own_str:
            return 1
        own_str = own_str.lower()
        if 'first' in own_str or '1st' in own_str: return 1
        if 'second' in own_str or '2nd' in own_str: return 2
        if 'third' in own_str or '3rd' in own_str: return 3
        
        # Try extracting number
        match = re.search(r'\d', own_str)
        if match: return int(match.group(0))
        return 1

    @staticmethod
    def normalize_fuel(fuel_str: str | None) -> str | None:
        if not fuel_str: return None
        fuel_str = fuel_str.lower()
        if 'petrol' in fuel_str: return 'Petrol'
        if 'diesel' in fuel_str: return 'Diesel'
        if 'cng' in fuel_str: return 'CNG'
        if 'electric' in fuel_str or 'ev' in fuel_str: return 'Electric'
        if 'hybrid' in fuel_str: return 'Hybrid'
        return fuel_str.capitalize()

    @staticmethod
    def normalize_transmission(trans_str: str | None) -> str | None:
        if not trans_str: return None
        trans_str = trans_str.lower()
        if 'auto' in trans_str or 'amt' in trans_str or 'cvt' in trans_str: return 'Automatic'
        if 'manual' in trans_str or 'mt' in trans_str: return 'Manual'
        return trans_str.capitalize()
