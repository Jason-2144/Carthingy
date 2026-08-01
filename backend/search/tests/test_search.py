import pytest
from backend.search.filters.parser import nl_parser
from backend.search.engine import search_engine

def test_natural_query_parser():
    # Test simple price extraction
    q1, f1 = nl_parser.parse("Toyota under 8 lakh")
    assert "toyota" in q1.lower()
    assert f1.get("price_max") == 800000

    # Test combined extraction
    q2, f2 = nl_parser.parse("Honda city automatic less than 5 years old under 50,000 km")
    assert "honda city" in q2.lower()
    assert f2.get("transmission") == "Automatic"
    assert "registration_year_min" in f2
    assert f2.get("km_driven_max") == 50000
    
def test_build_meili_filter():
    filters = {
        "price_max": 800000,
        "make": "Toyota",
        "transmission": ["Automatic", "Manual"],
        "registration_year_min": 2018
    }
    meili_filters = search_engine.build_meili_filter(filters)
    assert "price <= 800000" in meili_filters
    assert "make = 'Toyota'" in meili_filters
    assert "registration_year >= 2018" in meili_filters
    assert "(transmission = 'Automatic' OR transmission = 'Manual')" in meili_filters
