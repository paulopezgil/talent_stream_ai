from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.schemas.message import ChatRequest, MessageResponse
from backend.services import crud as crud_service
from backend.services.agent import generate_agent_response

router = APIRouter(prefix="/api/projects", tags=["messages"])



@router.get("/{project_id}/messages", response_model=List[MessageResponse])
async def get_project_messages(project_id: UUID, db: AsyncSession = Depends(get_db)):
    """Returns the entire conversation history for the project."""
    return await crud_service.messages.get_project_messages(db, project_id)

@router.post("/{project_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_project_message(project_id: UUID, request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Adds a new user message, invokes the AI agent, and returns the AI's response.
    The agent execution is a side-effect of posting a message.
    """
    # 1. Save user message to DB
    await crud_service.messages.create_message(db, project_id, "user", request.content)
    
    # 2. Invoke Agent (passing the prompt)
    agent_response_text = await generate_agent_response(db, project_id, request.content)
    
    # 3. Save and return assistant response
    return await crud_service.messages.create_message(db, project_id, "assistant", agent_response_text)

@router.put("/{project_id}/messages/last", response_model=MessageResponse)
async def update_last_message(project_id: UUID, request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Updates the last user message, deletes the subsequent assistant message (if any),
    and regenerates the AI's response.
    """
    all_msgs = await crud_service.messages.get_project_messages(db, project_id)
    if not all_msgs:
        raise HTTPException(status_code=400, detail="No messages to update")
        
    last_msg = all_msgs[-1]
    
    if last_msg.role == "assistant":
        # Delete the assistant message
        await crud_service.messages.delete_message(db, last_msg)
        if len(all_msgs) > 1 and all_msgs[-2].role == "user":
            user_msg = all_msgs[-2]
            await crud_service.messages.update_message(db, user_msg, request.content)
        else:
            # Edge case: only assistant message exists
            await crud_service.messages.create_message(db, project_id, "user", request.content)
    elif last_msg.role == "user":
        # Just update the user message directly
        await crud_service.messages.update_message(db, last_msg, request.content)
    else:
        raise HTTPException(status_code=400, detail="Cannot update this message state")
        
    # Invoke Agent with the new content
    agent_response_text = await generate_agent_response(db, project_id, request.content)
    
    # Save and return new assistant response
    return await crud_service.messages.create_message(db, project_id, "assistant", agent_response_text)
