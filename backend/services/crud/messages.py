from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.message import Message


async def get_project_messages(db: AsyncSession, project_id: UUID) -> List[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.project_id == project_id)
        .order_by(Message.created_at.asc())
    )
    return list(result.scalars().all())

async def get_message(db: AsyncSession, message_id: UUID) -> Optional[Message]:
    result = await db.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()

async def create_message(db: AsyncSession, project_id: UUID, role: str, content: str) -> Message:
    msg = Message(project_id=project_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def update_message(db: AsyncSession, msg: Message, content: str) -> Message:
    msg.content = content
    await db.commit()
    await db.refresh(msg)
    return msg

async def delete_message(db: AsyncSession, msg: Message) -> None:
    await db.delete(msg)
    await db.commit()
