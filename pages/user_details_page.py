from pages.base_page import BasePage


class UserDetailsPage(BasePage):
    def wait_until_loaded(self, username: str) -> None:
        # Profile name may render differently from login; use stable details markers.
        self.page.locator("p:has-text('repos')").first.wait_for()

        # Prefer verifying profile link points to the expected GitHub user.
        profile_link = self.page.locator(f"a[href*='github.com/{username}']")
        if profile_link.count() > 0:
            profile_link.first.wait_for()

    def get_repo_count_from_ui(self) -> int:
        repos_label = self.page.locator("p:has-text('repos')").first
        repo_count_text = repos_label.locator("xpath=..").locator("h3").first.inner_text()
        digits = "".join(ch for ch in repo_count_text if ch.isdigit())
        if not digits:
            raise AssertionError("Could not parse repository count from UI.")
        return int(digits)
