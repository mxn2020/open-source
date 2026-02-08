"""FastAPI application for the feature flag service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__, routes
from .database import FlagDatabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup."""
    routes.db = FlagDatabase()
    yield


app = FastAPI(
    title="Feature Flag Service",
    version=__version__,
    description="A feature flag management REST API for controlling feature rollouts.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("feature_flag_service.app:app", host="0.0.0.0", port=8000, reload=True)
