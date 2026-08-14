from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
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


@app.get("/")
def root():
    return {"name": "API Tracker", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
