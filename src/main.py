"""
KlartX — FastAPI main app, routers, lifespan
Contract ID: @app/router/lifespan
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import engine, get_session, Base
from src.auth import get_current_user, User

# ── Database init ─────────────────────────────────────────────────

def init_db():
    """Create all tables on startup."""
    Base.metadata.create_all(bind=engine)

# ── Lifespan ──────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# ── App ───────────────────────────────────────────────────────────

app = FastAPI(
    title="KlartX",
    description="Myndighetsdokument → plain-language → auto-fill → submit",
    version="0.1.0",
    lifespan=lifespan,
)

# Mount static files
STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Templates
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ── Health ────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ── Frontend ──────────────────────────────────────────────────────

@app.get("/")
async def index():
    with open(Path(__file__).parent.parent / "templates" / "index.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html)

# ── Upload (stub) ─────────────────────────────────────────────────

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Accept a PDF or image file. Returns 200 with a document_id."""
    # TODO: save file, trigger OCR pipeline
    return {"document_id": "stub", "filename": file.filename, "status": "uploaded"}

# ── Analyze (stub) ────────────────────────────────────────────────

@app.post("/analyze")
async def analyze_document(document_id: str = Form(...)):
    """Analyze a document with LLM. Returns summary + fields."""
    # TODO: trigger OCR → LLM parse
    return {
        "document_id": document_id,
        "summary": "Dokumentanalyserad (stub).",
        "key_points": ["Dokument mottaget", "Väntar på OCR"],
        "next_steps": ["Kontrollera fält", "Skicka in"],
    }

# ── Form (stub) ───────────────────────────────────────────────────

@app.post("/form")
async def get_form(document_id: str = Form(...)):
    """Auto-fill form for a document."""
    return {
        "form_id": "stub",
        "fields": [],
        "status": "filled",
    }

# ── Submit (stub) ─────────────────────────────────────────────────

@app.post("/submit")
async def submit_form(
    document_id: str = Form(...),
    bank_id_token: str = Form(None),
):
    """Submit a form via BankID."""
    return {
        "submission_id": "stub",
        "form_id": "stub",
        "case_id": "stub-case",
        "status": "submitted",
    }

# ── Track (stub) ──────────────────────────────────────────────────

@app.get("/track/{case_id}")
def track_case(case_id: str):
    """Track a case status."""
    return {
        "case_id": case_id,
        "status": "submitted",
        "updates": [],
    }
