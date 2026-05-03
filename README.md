# Playwright BDD + API tests

> Authored with Cursor AI assistance (Codex 5.3).

End-to-end and API automation using the **Playwright test runner** with **[playwright-bdd](https://github.com/vitalets/playwright-bdd)** for Gherkin features (Cucumber-style steps without losing Playwright reporting, traces, sharding, and fixtures).

## Layout

- `features/**/*.feature` — Gherkin scenarios
- `features/steps/*.ts` — step definitions (`createBdd` + Playwright `test` fixtures)
- `pages/*.ts` — page objects (TypeScript)
- `tests/api/*.spec.ts` — REST contract tests (`@playwright/test` `request` fixture)
- `playwright.config.ts` — two projects: **`chromium-bdd`** (generated from features) and **`api`**

## Setup

```bash
npm install
npx playwright install --with-deps chromium
```

After the first `npm install`, commit `package-lock.json` and you can switch CI to `npm ci` for reproducible installs.

## Run

All projects (BDD UI + API):

```bash
npm test
```

Only UI scenarios (after codegen):

```bash
npm run test:ui
```

Only API tests:

```bash
npm run test:api
```

Headed UI:

```bash
npx bddgen && npx playwright test --project=chromium-bdd --headed
```

Environment:

- `BASE_URL` — app under test (default: `https://gh-users-search.netlify.app`)
- `GITHUB_API_BASE` — GitHub REST root (default: `https://api.github.com`)
- `GITHUB_TOKEN` — optional; raises rate limits for API tests and BDD API assertions

## GitHub Actions

Workflow: `.github/workflows/playwright-bdd.yml` runs `npm test` (includes `bddgen` before `playwright test`).

## Current BDD scenario

Happy path for [gh-users-search.netlify.app](https://gh-users-search.netlify.app/): search `swangful`, assert UI public repo count matches live GitHub `public_repos`.
