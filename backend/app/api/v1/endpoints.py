from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from app.schemas import EmployeeProfile, EmployeeResult, ParsedEmployeeProfile, QueryRequest
from app.services.llm_service import parse_employee, parse_query
from app.services.qdrant_service import upsert_employee, search_employees

router = APIRouter()


@router.post("/employees/upload", response_model=dict[str, Any])
async def upload_employee(profile: EmployeeProfile):
    """Ingest an employee profile: extract metadata via LLM, embed, and store."""
    parsed = await parse_employee(profile)
    point_id = upsert_employee(parsed)

    return {
        "id": point_id,
        "parsed_profile": parsed.model_dump(),
        "message": "Employee profile ingested successfully.",
    }


@router.post("/query", response_model=list[EmployeeResult])
async def query_employees(req: QueryRequest):
    """Metadata-filtered vector search over employee profiles."""
    parsed = await parse_query(req.query)
    results = search_employees(parsed, req.query, req.top_k)
    return results


@router.get("/health")
async def health():
    return {"status": "ok"}
