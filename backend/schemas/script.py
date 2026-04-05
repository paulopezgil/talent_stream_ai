from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ScriptUpdate(BaseModel):
    content: Optional[str] = None

class ScriptResponse(BaseModel):
    id: UUID
    project_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
