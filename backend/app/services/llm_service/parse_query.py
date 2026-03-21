from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from app.schemas import ParsedQuery
from app.services.llm_service.clients import get_llm
from app.services.llm_service.prompt_templates import PARSE_QUERY_PROMPT_TEMPLATE

parse_query_prompt = ChatPromptTemplate.from_template(PARSE_QUERY_PROMPT_TEMPLATE)


async def parse_query(raw_query: str) -> ParsedQuery:
    """Use the LLM to decompose a hiring query into filters + semantic text."""
    try:
        chain = parse_query_prompt | get_llm().with_structured_output(ParsedQuery)
        return await chain.ainvoke({"query": raw_query})
    except Exception:
        return ParsedQuery(semantic_query=raw_query)
