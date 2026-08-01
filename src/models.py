"""
KlartX — Pydantic schemas (requests/responses)
Contract ID: @schemas/document/field/form
"""

from datetime import datetime
from typing import Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


# ── Document schemas ──────────────────────────────────────────────

class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    content_length: int


class DocumentResult(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    filename: str
    content_type: str
    text: Optional[str] = None
    status: str = "uploaded"  # uploaded | processed | error
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Field schemas ─────────────────────────────────────────────────

class FieldValue(BaseModel):
    field_name: str
    value: Any
    confidence: float = 1.0


class FieldList(BaseModel):
    fields: list[FieldValue] = []
    document_id: str


# ── Form schemas ──────────────────────────────────────────────────

class FormRequest(BaseModel):
    document_id: str
    bank_id_token: Optional[str] = None


class FormResponse(BaseModel):
    form_id: str = Field(default_factory=lambda: str(uuid4()))
    fields: list[dict[str, Any]] = []
    status: str = "filled"  # filled | submitted | error
    submitted_at: Optional[datetime] = None


class SubmitResponse(BaseModel):
    submission_id: str = Field(default_factory=lambda: str(uuid4()))
    form_id: str
    case_id: str = Field(default_factory=lambda: str(uuid4()))
    status: str = "submitted"
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


# ── Tracking schemas ──────────────────────────────────────────────

class TrackingStatus(BaseModel):
    case_id: str
    status: str  # submitted | in_review | decision_pending | completed
    updates: list[dict[str, Any]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str] = []
    next_steps: list[str] = []
