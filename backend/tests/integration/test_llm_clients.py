from __future__ import annotations

import pytest

from app.core.config import settings
from app.services.llm_service.clients import get_embeddings, get_llm

pytestmark = pytest.mark.skipif(
    not settings.openai_api_key,
    reason="OPENAI_API_KEY not set — skipping live LLM client tests",
)


def test_llm_client_instantiates():
    llm = get_llm()
    assert llm.model_name == "gpt-4o-mini"
    assert llm.temperature == 0


def test_llm_client_completes_simple_prompt():
    llm = get_llm()
    response = llm.invoke("Reply with the single word: pong")
    assert isinstance(response.content, str)
    assert len(response.content) > 0


def test_embeddings_client_instantiates():
    embeddings = get_embeddings()
    assert embeddings.model == "text-embedding-ada-002"


def test_embeddings_client_returns_correct_dimension():
    embeddings = get_embeddings()
    vector = embeddings.embed_query("hello world")
    assert isinstance(vector, list)
    assert len(vector) == 1536
    assert all(isinstance(v, float) for v in vector)
