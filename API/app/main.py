from fastapi import FastAPI

from app.dbconfig.config import IS_PRODUCTION
from app.routers import public


app = FastAPI(
    title="Football team API",
    description="API for fetching football team players",
    version="1.0.1",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json"
)

app.include_router(public.router)
