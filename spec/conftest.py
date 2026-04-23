import os

import pytest
import requests


@pytest.fixture(scope="session")
def api_base() -> str:
    return os.getenv("GITHUB_API_BASE", "https://api.github.com").rstrip("/")


@pytest.fixture(scope="session")
def github_session(api_base: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "playwright-test-framework (API spec tests)",
        }
    )
    token = os.getenv("GITHUB_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    return session
