from pages.base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = "input[type='text'], input[placeholder*='Search']"
    SEARCH_BUTTON = "button:has-text('Search')"

    def open(self, base_url: str) -> None:
        self.goto(base_url)

    def search_user(self, username: str) -> None:
        search_input = self.page.locator(self.SEARCH_INPUT).first
        search_input.fill(username)
        if self.page.locator(self.SEARCH_BUTTON).count() > 0:
            self.page.locator(self.SEARCH_BUTTON).first.click()
        else:
            search_input.press("Enter")
        # Wait for requested profile data to load before next step.
        self.page.locator(f"a[href*='github.com/{username}']").first.wait_for()

    def click_user_result(self, username: str) -> None:
        # This app auto-loads user details after search; avoid clicking external links.
        user_text = self.page.get_by_text(username, exact=False)
        if user_text.count() > 0:
            return

        repos_label = self.page.get_by_text("Repos", exact=False)
        if repos_label.count() > 0:
            return

        raise AssertionError(f"Could not find user result for '{username}'.")
