from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up")
    yield
    # shutdown: cleanup
    print("shutting down")


app = FastAPI(
    title="Image Analyzer",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")