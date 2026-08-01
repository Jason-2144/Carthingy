# Deal Intelligence Engine

The Deal Intelligence Engine is a comprehensive dealer-grade recommendation and pricing system designed to rank, evaluate, and provide actionable insights on every used car listing.

## Architecture

* **scoring/**: Calculates a 0-100 `Deal Score` based on configurable weights (difference from market value, mileage, age, ownership, demand, price drops, days on market).
* **recommendations/**: Maps the 0-100 score into actionable human-readable categories (e.g., "Exceptional Deal", "Fair Price", "Avoid") and provides textual explanations.
* **ranking/**: `SimilarityEngine` finds the top similar vehicles using a weighted distance formula (matching make, model, variant, and calculating proximity for year, km_driven, fuel, transmission).
* **pricing/**:
  * `NegotiationEngine`: Estimates how much negotiation room exists based on whether the car is overpriced and how long it has been on the market.
  * `DealerProfitCalculator`: Calculates purchase price targets, break-even points, and expected ROI assuming configurable reconditioning, transport, and registration costs.
* **analytics/**:
  * `MarketDemandEngine`: Real-time calculation of active listings, days on market, and demand vs supply metrics.
  * `DealerInsightsEngine`: Identifies specific opportunities such as Fast Flips (undervalued high-demand cars) and Hidden Gems (old listings with price drops).
* **jobs/**: Celery tasks to asynchronously recalculate deal scores and generate insight reports.
* **tests/**: Unit testing for all algorithms and calculators.

## Configuration

Configuration is managed via Pydantic Settings in `config.py` (`DealEngineSettings`).
Admins can tweak these weights dynamically using environment variables without modifying code.

### Deal Score Weights (Total ~1.0)
* `DEAL_WEIGHT_VALUATION_DIFF`: 40%
* `DEAL_WEIGHT_MILEAGE`: 15%
* `DEAL_WEIGHT_AGE`: 10%
* `DEAL_WEIGHT_OWNERSHIP`: 5%
* `DEAL_WEIGHT_DAYS_ON_MARKET`: 10%
* `DEAL_WEIGHT_DEMAND`: 10%
* `DEAL_WEIGHT_PRICE_DROPS`: 5%
* `DEAL_WEIGHT_SELLER_RELIABILITY`: 5%

### Dealer Profit Constants
* `DEAL_RECONDITIONING_COST_BASE`: Base reconditioning cost (default 15000)
* `DEAL_TRANSPORT_COST_BASE`: Base transport cost (default 5000)
* `DEAL_REGISTRATION_COST_BASE`: Base RTO cost (default 2000)
* `DEAL_DEALER_TARGET_MARGIN`: Target profit margin % (default 10%)

## API Endpoints

All endpoints are prefixed with `/api/v1/deal-intelligence/`

* `POST /analyze`: Evaluates a vehicle (first calling the Valuation Engine, then running all Deal Intelligence components) to return a full deal report (Score, Recommendation, Negotiation margins, Dealer profit estimate, Market demand).
* `GET /similar/{listing_id}`: Returns the top 20 similar vehicles and their similarity score.
* `GET /insights/hidden-gems`: Returns heavily-discounted/old listings.
* `GET /insights/fast-flips`: Returns recently posted, under-market listings.
* `POST /jobs/recalculate`: Triggers background recalculation tasks.

## Usage

```python
from backend.deal_engine.engine import deal_engine

report = await deal_engine.analyze_listing(listing_data, estimated_market_value)
print(report["deal_score"])
print(report["recommendation"]["classification"])
```
