import type { Page } from '@playwright/test';
import { BasePage } from './BasePage.js';

export class HomePage extends BasePage {
  private static readonly SEARCH_INPUT =
    "input[type='text'], input[placeholder*='Search']";
  private static readonly SEARCH_BUTTON = "button:has-text('Search')";

  constructor(page: Page) {
    super(page);
  }

  async open(path = '/'): Promise<void> {
    await this.goto(path);
  }

  async searchUser(username: string): Promise<void> {
    const searchInput = this.page.locator(HomePage.SEARCH_INPUT).first();
    await searchInput.fill(username);
    const searchBtn = this.page.locator(HomePage.SEARCH_BUTTON);
    if ((await searchBtn.count()) > 0) {
      await searchBtn.first().click();
    } else {
      await searchInput.press('Enter');
    }
    await this.page.locator(`a[href*='github.com/${username}']`).first().waitFor();
  }

  async clickUserResult(username: string): Promise<void> {
    const userText = this.page.getByText(username, { exact: false });
    if ((await userText.count()) > 0) {
      return;
    }
    const repos = this.page.getByText('Repos', { exact: false });
    if ((await repos.count()) > 0) {
      return;
    }
    throw new Error(`Could not find user result for '${username}'.`);
  }
}
