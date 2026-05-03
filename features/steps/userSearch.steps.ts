import { expect } from '@playwright/test';
import { HomePage } from '../../pages/HomePage.js';
import { UserDetailsPage } from '../../pages/UserDetailsPage.js';
import { Given, Then, When } from './fixtures.js';

const GITHUB_API_BASE = (process.env.GITHUB_API_BASE ?? 'https://api.github.com').replace(
  /\/$/,
  '',
);

const githubRequestHeaders = {
  Accept: 'application/vnd.github+json',
  'X-GitHub-Api-Version': '2022-11-28',
  'User-Agent': 'playwright-test-bdd (BDD steps)',
  ...(process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {}),
};

Given('I open the GitHub user search application', async ({ page }) => {
  const home = new HomePage(page);
  await home.open('/');
});

When('I search for github user {string}', async ({ page }, username: string) => {
  const home = new HomePage(page);
  await home.searchUser(username);
});

When('I open {string} from the results', async ({ page }, username: string) => {
  const home = new HomePage(page);
  await home.clickUserResult(username);
});

Then('I should see {string} profile details', async ({ page }, username: string) => {
  const details = new UserDetailsPage(page);
  await details.waitUntilLoaded(username);
});

Then(
  'the UI repository count should match GitHub public_repos for {string}',
  async ({ page, request }, username: string) => {
    const details = new UserDetailsPage(page);
    const apiUser = await request.get(`${GITHUB_API_BASE}/users/${username}`, {
      headers: githubRequestHeaders,
    });
    if (!apiUser.ok()) {
      throw new Error(`GitHub API ${apiUser.status()}: ${await apiUser.text()}`);
    }
    const body = (await apiUser.json()) as { public_repos?: number };
    const apiCount = body.public_repos;
    expect(apiCount, 'API public_repos missing').toBeDefined();
    const uiCount = await details.getRepoCountFromUi();
    expect(
      uiCount,
      `UI showed ${uiCount} public repos but GitHub API public_repos is ${apiCount} for '${username}'.`,
    ).toBe(apiCount);
  },
);
