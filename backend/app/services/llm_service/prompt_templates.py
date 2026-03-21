from __future__ import annotations

PARSE_EMPLOYEE_PROMPT_TEMPLATE = """
You are a metadata extraction assistant.
Given an employee profile, extract structured data.

Employee profile:
```{profile_text}```
""".strip()

PARSE_QUERY_PROMPT_TEMPLATE = """
You are a query-understanding assistant for a talent search engine.
Given a natural-language hiring query, extract filter parameters.

Hiring query:
```{query}```
""".strip()
