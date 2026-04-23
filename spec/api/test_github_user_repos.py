"""GitHub REST API: GET /users/{username}/repos — public repositories for a user."""


def _assert_json_array_response(response):
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    return data


def test_list_public_repos_matches_public_repos_count(github_session, api_base):
    user = github_session.get(f"{api_base}/users/swangful", timeout=30)
    assert user.status_code == 200
    expected = user.json()["public_repos"]

    repos = github_session.get(
        f"{api_base}/users/swangful/repos",
        params={"per_page": 100, "type": "owner"},
        timeout=30,
    )
    data = _assert_json_array_response(repos)
    assert len(data) == expected


def test_list_repos_returns_expected_repo_fields(github_session, api_base):
    response = github_session.get(
        f"{api_base}/users/swangful/repos",
        params={"per_page": 5},
        timeout=30,
    )
    data = _assert_json_array_response(response)
    assert len(data) >= 1
    repo = data[0]
    for key in ("name", "full_name", "html_url", "private", "stargazers_count"):
        assert key in repo


def test_list_repos_for_unknown_user_404(github_session, api_base):
    response = github_session.get(
        f"{api_base}/users/this-login-should-not-exist-404-xyz/repos",
        timeout=30,
    )
    assert response.status_code == 404


def test_list_repos_accepts_sort_and_direction(github_session, api_base):
    response = github_session.get(
        f"{api_base}/users/swangful/repos",
        params={"per_page": 5, "sort": "updated", "direction": "desc"},
        timeout=30,
    )
    _assert_json_array_response(response)
