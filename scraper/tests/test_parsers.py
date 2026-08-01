import pytest
from scraper.normalizers.car import CarNormalizer
from scraper.parsers.olx import OLXParser

def test_normalize_price():
    assert CarNormalizer.normalize_price("₹ 5,00,000") == 500000.0
    assert CarNormalizer.normalize_price("500000") == 500000.0
    assert CarNormalizer.normalize_price(None) is None

def test_normalize_mileage():
    assert CarNormalizer.normalize_mileage("45,000 km") == 45000
    assert CarNormalizer.normalize_mileage("45k") == 45000

def test_olx_parser():
    raw_data = {
        "url": "https://www.olx.in/item/iid-12345",
        "marketplace": "OLX",
        "title": "Maruti Suzuki Swift Dzire",
        "price": "₹ 6,50,000",
        "attributes": ["Brand", "Maruti Suzuki", "Model", "Swift Dzire", "Year", "2018", "KM driven", "45,000 km", "Fuel", "Petrol", "Transmission", "Manual"],
    }
    
    parser = OLXParser()
    parsed = parser.parse(raw_data)
    
    assert parsed["external_listing_id"] == "12345"
    assert parsed["price"] == 650000.0
    assert parsed["make"] == "Maruti Suzuki"
    assert parsed["model"] == "Swift Dzire"
    assert parsed["registration_year"] == 2018
    assert parsed["km_driven"] == 45000
    assert parsed["fuel"] == "Petrol"
    assert parsed["transmission"] == "Manual"
