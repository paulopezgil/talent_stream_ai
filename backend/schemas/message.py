from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ChatRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: UUID
    project_id: UUID
    role: str
    content: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
