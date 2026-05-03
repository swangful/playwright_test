import type { Page } from '@playwright/test';
import { BasePage } from './BasePage.js';

export class UserDetailsPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async waitUntilLoaded(username: string): Promise<void> {
    await this.page.locator("p:has-text('repos')").first().waitFor();
    const profileLink = this.page.locator(`a[href*='github.com/${username}']`);
    if ((await profileLink.count()) > 0) {
      await profileLink.first().waitFor();
    }
  }

  async getRepoCountFromUi(): Promise<number> {
    const reposLabel = this.page.locator("p:has-text('repos')").first();
    const repoCountText = await reposLabel
      .locator('xpath=..')
      .locator('h3')
      .first()
      .innerText();
    const digits = [...repoCountText].filter((ch) => /\d/.test(ch)).join('');
    if (!digits) {
      throw new Error('Could not parse repository count from UI.');
    }
    return parseInt(digits, 10);
  }
}
