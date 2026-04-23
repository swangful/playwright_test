# Playwright Python BDD Framework (POM + Slack + GitHub Actions)

> Authored with Cursor AI assistance (Codex 5.3).

This project provides a Python test automation framework using:
- **Playwright** for browser automation
- **Behave** (Cucumber for Python) for BDD
- **Page Object Model (POM)** for maintainable UI abstractions
- **Slack webhook reporting** for test notifications
- **GitHub Actions** for CI execution

## Project Structure

- `spec/` - Pytest API contract tests (GitHub REST API used by the app)
- `features/` - BDD feature files
- `features/steps/` - Behave step definitions
- `features/environment.py` - Behave hooks (browser lifecycle + Slack reporting)
- `pages/` - Page objects
- `utils/` - Helpers (config + Slack notifier)
- `config/` - Runtime configuration
- `reports/` - Generated test reports
- `.github/workflows/` - CI workflow

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium
```

## Run Tests

```bash
behave
```

API tests (no browser):

```bash
pytest
```

Optional: higher rate limits with a token:

```bash
export GITHUB_TOKEN="ghp_..."
pytest
```

Run with environment overrides:

```bash
BASE_URL="https://gh-users-search.netlify.app" HEADLESS="true" behave
```

## Slack Integration

Add a webhook URL (local shell):

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

Or configure in GitHub Actions secret:
- `SLACK_WEBHOOK_URL`

## GitHub Actions

Workflow file: `.github/workflows/playwright-bdd.yml`

It installs dependencies, installs Playwright Chromium, runs Behave tests, uploads reports, and posts summary to Slack.

## Initial Automated Scenario

Implemented happy path:
1. Search for `swangful`
2. Open user details from search results
3. Assert the UI public repository count matches GitHub `public_repos` for that user (stable as the account changes)
