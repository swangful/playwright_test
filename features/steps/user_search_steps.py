import requests
from behave import given, then, when

from config.settings import GITHUB_API_BASE
from pages.home_page import HomePage
from pages.user_details_page import UserDetailsPage


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
    user_response = requests.get(f"{GITHUB_API_BASE}/users/{username}", timeout=10)
    user_response.raise_for_status()
    user_data = user_response.json()

    actual_count = user_data.get("public_repos")
    assert actual_count == expected_count, (
        f"Expected {expected_count} repositories from API, but got {actual_count}."
    )
