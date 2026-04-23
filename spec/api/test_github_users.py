"""GitHub REST API: GET /users/{username} — mirrors data the Netlify app displays."""

import pytest


def _assert_json_response_headers(response):
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert "x-ratelimit-limit" in {k.lower() for k in response.headers}
    assert "x-ratelimit-remaining" in {k.lower() for k in response.headers}


@pytest.mark.parametrize("login", ["swangful", "octocat"])
def test_get_user_success(github_session, api_base, login):
    response = github_session.get(f"{api_base}/users/{login}", timeout=30)
    assert response.status_code == 200
    _assert_json_response_headers(response)
    body = response.json()
    assert body["login"].lower() == login.lower()
    assert isinstance(body["id"], int)
    assert body["type"] == "User"
    assert "public_repos" in body
    assert isinstance(body["public_repos"], int)


def test_get_user_not_found(github_session, api_base):
    response = github_session.get(
        f"{api_base}/users/this-login-should-not-exist-404-xyz",
        timeout=30,
    )
    assert response.status_code == 404
    _assert_json_response_headers(response)
    body = response.json()
    assert "message" in body


def test_get_user_invalid_login_returns_404(github_session, api_base):
    response = github_session.get(f"{api_base}/users/!!!not-a-valid-login!!!", timeout=30)
    assert response.status_code == 404


def test_get_user_response_includes_useful_headers(github_session, api_base):
    response = github_session.get(f"{api_base}/users/octocat", timeout=30)
    assert response.status_code == 200
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert "x-github-request-id" in headers_lower or "x-github-request-id" in response.headers
    assert headers_lower.get("content-type", "").startswith("application/json")


def test_get_user_etag_supports_conditional_request(github_session, api_base):
    first = github_session.get(f"{api_base}/users/octocat", timeout=30)
    assert first.status_code == 200
    etag = first.headers.get("ETag") or first.headers.get("etag")
    if not etag:
        pytest.skip("No ETag returned for this response; cannot assert caching behavior.")
    second = github_session.get(
        f"{api_base}/users/octocat",
        headers={"If-None-Match": etag},
        timeout=30,
    )
    assert second.status_code == 304
