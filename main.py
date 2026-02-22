"""
ZenithDUS — Main Entry Point
==============================
Her şeyi bir araya getirir: FastAPI + DB + Seed Data + CORS
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from src.infrastructure.database.supabase_client import create_tables, SessionLocal
from src.infrastructure.seed_data import seed_database
from src.presentation.api import router

app = FastAPI(
    title="ZenithDUS API",
    description="🦷 AI-Powered Adaptive DUS Platform",
    version="1.0.0",
)

# CORS — React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup():
    print("🦷 ZenithDUS başlatılıyor...")
    create_tables()
    print("✅ Tablolar oluşturuldu.")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    print("🚀 ZenithDUS hazır! → http://localhost:8000/docs")


@app.get("/")
def root():
    return {"message": "🦷 ZenithDUS API — /docs sayfasını ziyaret edin"}
