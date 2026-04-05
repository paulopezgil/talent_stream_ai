from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.schemas.social_media import SocialMediaUpdate, SocialMediaResponse
from backend.services import crud as crud_service

router = APIRouter(prefix="/api/projects", tags=["social-media"])

@router.get("/{project_id}/social-media", response_model=Optional[SocialMediaResponse])
async def get_project_social_media(project_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud_service.social_media.get_project_social_media(db, project_id)

@router.put("/{project_id}/social-media", response_model=SocialMediaResponse)
async def update_or_create_social_media(project_id: UUID, sm_in: SocialMediaUpdate, db: AsyncSession = Depends(get_db)):
    sm = await crud_service.social_media.get_project_social_media(db, project_id)
    if not sm:
        # Create it (Upsert)
        return await crud_service.social_media.create_social_media(db, project_id, sm_in)
        
    return await crud_service.social_media.update_social_media(db, sm, sm_in)
