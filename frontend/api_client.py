import requests

from config import API_URL


def upload_employee(payload: dict) -> dict:
    resp = requests.post(f"{API_URL}/employees/upload", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_talent(query: str, top_k: int) -> list:
    resp = requests.post(
        f"{API_URL}/query", json={"query": query, "top_k": top_k}, timeout=30
    )
    resp.raise_for_status()
    return resp.json()
