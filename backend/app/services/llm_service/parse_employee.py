from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from app.schemas import EmployeeExtraction, EmployeeProfile, ParsedEmployeeProfile
from app.services.llm_service.clients import get_llm
from app.services.llm_service.prompt_templates import PARSE_EMPLOYEE_PROMPT_TEMPLATE

parse_employee_prompt = ChatPromptTemplate.from_template(PARSE_EMPLOYEE_PROMPT_TEMPLATE)


async def parse_employee(profile: EmployeeProfile) -> ParsedEmployeeProfile:
    """Use the LLM to extract skills and experience from the employee bio."""
    try:
        chain = parse_employee_prompt | get_llm().with_structured_output(EmployeeExtraction)
        parsed = await chain.ainvoke({"profile_text": profile.bio})
    except Exception:
        parsed = EmployeeExtraction()

    data = parsed.model_dump()
    return ParsedEmployeeProfile(
        **profile.model_dump(),
        skills=data.get("skills", []),
        years_experience=data.get("years_experience"),
    )
