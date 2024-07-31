from fastapi import FastAPI
from src.api import health, search

# initialization
app = FastAPI(docs_url="/docs", redoc_url=None)
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(search.router, prefix="/search", tags=["search"])
