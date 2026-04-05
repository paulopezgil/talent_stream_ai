from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.schemas.script import ScriptUpdate, ScriptResponse
from backend.services import crud as crud_service

router = APIRouter(prefix="/api/projects", tags=["scripts"])

@router.get("/{project_id}/script", response_model=Optional[ScriptResponse])
async def get_project_script(project_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud_service.scripts.get_project_script(db, project_id)

@router.put("/{project_id}/script", response_model=ScriptResponse)
async def update_or_create_script(project_id: UUID, script_in: ScriptUpdate, db: AsyncSession = Depends(get_db)):
    script = await crud_service.scripts.get_project_script(db, project_id)
    if not script:
        # Create it (Upsert)
        return await crud_service.scripts.create_script(db, project_id, script_in.content or "")
        
    return await crud_service.scripts.update_script(db, script, script_in)
