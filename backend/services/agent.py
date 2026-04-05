from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_ai import Agent, RunContext

from backend.services.crud.projects import get_project, update_project
from backend.services.crud.scripts import get_project_script, create_script, update_script
from backend.services.crud.social_media import get_project_social_media, create_social_media, update_social_media
from backend.schemas.project import ProjectUpdate
from backend.schemas.script import ScriptUpdate
from backend.schemas.social_media import SocialMediaUpdate

@dataclass
class ProjectAgentDeps:
    db: AsyncSession
    project_id: UUID

# Initialize the Pydantic AI agent
vidplan_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=ProjectAgentDeps,
    retries=2,
    system_prompt="""
    You are VidPlan AI, a helpful content creator assistant.
    You help brainstorm, plan, and generate video scripts and social media posts.
    You have the ability to read the current project context and update the project, script, and social media tabs.
    When asked to generate or update content, use the provided tools to save your work to the database.
    Always be concise, creative, and professional.
    """.strip()
)

@vidplan_agent.system_prompt
async def add_dynamic_context(ctx: RunContext[ProjectAgentDeps]) -> str:
    """Injects the current database state of the project into the system prompt."""
    db = ctx.deps.db
    project_id = ctx.deps.project_id
    
    project = await get_project(db, project_id)
    script = await get_project_script(db, project_id)
    sm = await get_project_social_media(db, project_id)
    
    context = ["Here is the current state of the user's workspace:"]
    
    if project:
        context.append(f"\n--- Project Tab ---\nTitle: {project.title}\nDescription: {project.description}")
        
    if script:
        context.append(f"\n--- Script Tab ---\nContent: {script.content}")
    else:
        context.append("\n--- Script Tab ---\nNo script generated yet.")
        
    if sm:
        context.append(f"\n--- Social Network Tab ---\nYouTube Title: {sm.youtube_title}\nYouTube Description: {sm.youtube_description}\nTwitter Post: {sm.twitter_post}\nLinkedIn Post: {sm.linkedin_post}")
    else:
        context.append("\n--- Social Network Tab ---\nNo social media content generated yet.")
        
    context.append("\nUse your tools to update these tabs when requested or when you generate new content.")
    return "\n".join(context)

@vidplan_agent.tool
async def update_project_tab(ctx: RunContext[ProjectAgentDeps], title: str, description: str) -> str:
    """Updates the project title and description in the database (Project Tab)."""
    db = ctx.deps.db
    project_id = ctx.deps.project_id
    project = await get_project(db, project_id)
    if not project:
        return "Failed to find project."
    
    update_data = ProjectUpdate(title=title, description=description)
    await update_project(db, project, update_data)
    return "Project Tab updated successfully."

@vidplan_agent.tool
async def update_script_tab(ctx: RunContext[ProjectAgentDeps], content: str) -> str:
    """Updates or creates the script content in the database (Script Tab)."""
    db = ctx.deps.db
    project_id = ctx.deps.project_id
    script = await get_project_script(db, project_id)
    
    if script:
        update_data = ScriptUpdate(content=content)
        await update_script(db, script, update_data)
    else:
        await create_script(db, project_id, content)
        
    return "Script Tab updated successfully."

@vidplan_agent.tool
async def update_social_media_tab(
    ctx: RunContext[ProjectAgentDeps], 
    youtube_title: Optional[str] = None,
    youtube_description: Optional[str] = None,
    instagram_description: Optional[str] = None,
    tiktok_description: Optional[str] = None,
    twitter_post: Optional[str] = None,
    linkedin_post: Optional[str] = None
) -> str:
    """Updates or creates the social media content in the database (Social Network Tab)."""
    db = ctx.deps.db
    project_id = ctx.deps.project_id
    sm = await get_project_social_media(db, project_id)
    
    if sm:
        update_data = SocialMediaUpdate(
            youtube_title=youtube_title,
            youtube_description=youtube_description,
            instagram_description=instagram_description,
            tiktok_description=tiktok_description,
            twitter_post=twitter_post,
            linkedin_post=linkedin_post
        )
        await update_social_media(db, sm, update_data)
    else:
        update_data = SocialMediaUpdate(
            youtube_title=youtube_title,
            youtube_description=youtube_description,
            instagram_description=instagram_description,
            tiktok_description=tiktok_description,
            twitter_post=twitter_post,
            linkedin_post=linkedin_post
        )
        await create_social_media(db, project_id, update_data)
        
    return "Social Network Tab updated successfully."


from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart
from backend.services.crud.messages import get_project_messages

def build_message_history(db_messages: list) -> list[ModelMessage]:
    """Convert DB messages to Pydantic AI ModelMessage history."""
    history = []
    for msg in db_messages:
        if msg.role == "user":
            history.append(ModelRequest(parts=[TextPart(content=msg.content)]))
        elif msg.role == "assistant":
            history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return history

async def generate_agent_response(db: AsyncSession, project_id: UUID, user_prompt: str) -> str:
    """
    Orchestrates the AI invocation.
    Fetches the sliding window of history, formats it, and runs the agent.
    """
    # Fetch all messages
    all_msgs = await get_project_messages(db, project_id)
    
    # Exclude the current user message which was just saved to DB by the router
    # We take up to 10 messages before the current one for the sliding window
    history_msgs = [m for m in all_msgs if m.role in ("user", "assistant")]
    if history_msgs and history_msgs[-1].role == "user" and history_msgs[-1].content == user_prompt:
        history_msgs = history_msgs[:-1] # Remove the current prompt from history
        
    # Take the last 10 messages for context
    history_window = history_msgs[-10:] if len(history_msgs) > 10 else history_msgs
    
    history = build_message_history(history_window)
    deps = ProjectAgentDeps(db=db, project_id=project_id)
    
    result = await vidplan_agent.run(user_prompt, deps=deps, message_history=history)
    return result.data
