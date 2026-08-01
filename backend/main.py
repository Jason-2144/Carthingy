from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from backend.core.config import settings
from backend.middleware.logging import RequestLoggingMiddleware

from backend.api.routers import auth, listings, analytics, admin, health
from backend.valuation.router import router as valuation_router
from backend.deal_engine.router import router as deal_router
from backend.search.router import router as search_router
from backend.operations.router import router as ops_router
from backend.ai.router import router as ai_router
from backend.api.mobile.router import router as mobile_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Enterprise Used Car Intelligence Platform Backend API",
    version="1.0.0",
)

# Middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(listings.router, prefix=f"{settings.API_V1_STR}/listings", tags=["Listings"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(valuation_router, prefix=f"{settings.API_V1_STR}/valuation", tags=["Valuation"])
app.include_router(deal_router, prefix=f"{settings.API_V1_STR}/deal-intelligence", tags=["Deal Intelligence"])
app.include_router(search_router, prefix=f"{settings.API_V1_STR}/search", tags=["Search Engine"])
app.include_router(ops_router, prefix=f"{settings.API_V1_STR}/operations", tags=["Operations Platform"])
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI Copilot"])
app.include_router(mobile_router, tags=["Mobile API"])

@app.get("/")
def root():
    return {"message": "Welcome to CarScope AI API. Visit /docs for API documentation."}
