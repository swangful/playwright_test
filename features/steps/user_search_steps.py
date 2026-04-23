import requests
from behave import given, then, when

from config.settings import GITHUB_API_BASE
from pages.home_page import HomePage
from pages.user_details_page import UserDetailsPage

_GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "playwright-test-bdd (Behave)",
}


@given("I open the GitHub user search application")
def step_open_app(context):
    context.home_page = HomePage(context.page)
    context.user_details_page = UserDetailsPage(context.page)
    context.home_page.open(context.base_url)


@when('I search for github user "{username}"')
def step_search_user(context, username):
    context.searched_username = username
    context.home_page.search_user(username)


@when('I open "{username}" from the results')
def step_open_result(context, username):
    context.home_page.click_user_result(username)


@then('I should see "{username}" profile details')
def step_profile_loaded(context, username):
    context.user_details_page.wait_until_loaded(username)


@then("I should see {expected_count:d} repositories in the UI")
def step_verify_ui_repo_count(context, expected_count):
    actual_count = context.user_details_page.get_repo_count_from_ui()
    assert actual_count == expected_count, (
        f"Expected {expected_count} repositories in UI, but got {actual_count}."
    )


@then('the API should report {expected_count:d} repositories for "{username}"')
def step_verify_api_repo_count(context, expected_count, username):
    user_response = requests.get(
        f"{GITHUB_API_BASE}/users/{username}",
        headers=_GITHUB_HEADERS,
        timeout=10,
    )
    user_response.raise_for_status()
    user_data = user_response.json()

    actual_count = user_data.get("public_repos")
    assert actual_count == expected_count, (
        f"Expected {expected_count} repositories from API, but got {actual_count}."
    )


@then('the UI repository count should match GitHub public_repos for "{username}"')
def step_ui_repo_count_matches_github(context, username):
    user_response = requests.get(
        f"{GITHUB_API_BASE}/users/{username}",
        headers=_GITHUB_HEADERS,
        timeout=10,
    )
    user_response.raise_for_status()
    api_count = user_response.json().get("public_repos")
    ui_count = context.user_details_page.get_repo_count_from_ui()
    assert ui_count == api_count, (
        f"UI showed {ui_count} public repos but GitHub API public_repos is {api_count} for '{username}'."
    )
