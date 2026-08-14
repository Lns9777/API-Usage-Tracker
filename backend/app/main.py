from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .paths import get_frontend_dist_dir
from .routes import analytics, models, pricing, projects, providers, usage

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Tracker", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(usage.router)
app.include_router(pricing.router)
app.include_router(providers.router)
app.include_router(models.router)
app.include_router(analytics.router)

frontend_dist = get_frontend_dist_dir()
index_file = frontend_dist / "index.html"
assets_dir = frontend_dist / "assets"

if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/")
def root():
    if index_file.exists():
        return FileResponse(index_file)
    return {"name": "API Tracker", "status": "running"}


@app.get("/{path:path}")
def frontend_fallback(path: str):
    target = frontend_dist / path
    if target.exists() and target.is_file():
        return FileResponse(target)
    if index_file.exists():
        return FileResponse(index_file)
    return {"detail": "frontend not built"}


@app.get("/health")
def health():
    return {"status": "healthy"}
