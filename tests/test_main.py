"""Tests for KlartX main app."""

import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.fixture
def client():
    """Create a test async client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health(client):
    """Health check returns 200."""
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_index(client):
    """Index page returns 200 with HTML."""
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_upload_stubs(client):
    """Upload returns 200 with stub data."""
    resp = await client.post(
        "/upload",
        files={"file": ("test.pdf", b"fake pdf content", "application/pdf")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "uploaded"
    assert data["filename"] == "test.pdf"


@pytest.mark.asyncio
async def test_analyze_stubs(client):
    """Analyze returns 200 with summary."""
    resp = await client.post("/analyze", data={"document_id": "doc1"})
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data
    assert data["document_id"] == "doc1"


@pytest.mark.asyncio
async def test_form_stubs(client):
    """Form returns 200 with fields."""
    resp = await client.post("/form", data={"document_id": "doc1"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "filled"


@pytest.mark.asyncio
async def test_submit_stubs(client):
    """Submit returns 200 with submission_id."""
    resp = await client.post("/submit", data={"document_id": "doc1"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "submitted"
    assert "submission_id" in data


@pytest.mark.asyncio
async def test_track_stubs(client):
    """Track returns 200 with case status."""
    resp = await client.get("/track/case123")
    assert resp.status_code == 200
    data = resp.json()
    assert data["case_id"] == "case123"
    assert data["status"] == "submitted"
