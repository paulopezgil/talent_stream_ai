from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.schemas.project import ProjectUpdate, ProjectResponse, ProjectListResponse
from backend.services import crud as crud_service


router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[ProjectListResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    return await crud_service.projects.get_projects(db)

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(db: AsyncSession = Depends(get_db)):
    return await crud_service.projects.create_project(db)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    project = await crud_service.projects.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, project_in: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    project = await crud_service.projects.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await crud_service.projects.update_project(db, project, project_in)
