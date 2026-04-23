"""GitHub REST API: GET /search/users — typical backing call for user search UIs."""


def _assert_json_response_headers(response):
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert "x-ratelimit-limit" in {k.lower() for k in response.headers}


def test_search_users_finds_swangful(github_session, api_base):
    response = github_session.get(
        f"{api_base}/search/users",
        params={"q": "swangful"},
        timeout=30,
    )
    assert response.status_code == 200
    _assert_json_response_headers(response)
    body = response.json()
    assert "items" in body
    assert isinstance(body["items"], list)
    logins = {item["login"].lower() for item in body["items"]}
    assert "swangful" in logins


def test_search_users_empty_query_validation(github_session, api_base):
    response = github_session.get(
        f"{api_base}/search/users",
        params={"q": ""},
        timeout=30,
    )
    assert response.status_code == 422
    body = response.json()
    assert "message" in body


def test_search_users_requires_authentication_for_high_volume(github_session, api_base):
    """Unauthenticated search is allowed but heavily rate-limited; ensure we get a coherent response."""
    response = github_session.get(
        f"{api_base}/search/users",
        params={"q": "location:San Francisco"},
        timeout=30,
    )
    assert response.status_code in (200, 403)
    if response.status_code == 200:
        _assert_json_response_headers(response)
        assert "total_count" in response.json()
