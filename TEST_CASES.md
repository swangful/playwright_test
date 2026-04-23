# Test Suite - gh-users-search.netlify.app

## UI Layer Test Cases

- UI-001: Load home page successfully and verify search controls are visible.
- UI-002: Search valid username and verify result card contains matching username.
- UI-003: Open user details from results and verify profile header is shown.
- UI-004: Verify repository count displayed in user details matches expected value from fixture/API.
- UI-005: Verify followers/following statistics are rendered for a known user.
- UI-006: Search with mixed-case username and verify case-insensitive handling.
- UI-007: Search unknown username and verify empty/error state message.
- UI-008: Search with empty string and verify validation behavior (button disabled or message).
- UI-009: Simulate API failure (if possible with network mocking) and verify user-friendly error state.
- UI-010: Verify keyboard flow (type username, press Enter, open first result).
- UI-011: Verify responsive layout for mobile viewport and desktop viewport.
- UI-012: Verify external GitHub profile/repositories links navigate correctly.

## API Layer Test Cases (GitHub API)

- API-001: `GET /users/{username}` returns HTTP 200 for existing user.
- API-002: `GET /users/{username}` returns key fields (`login`, `id`, `public_repos`, `followers`).
- API-003: `GET /users/{username}` returns HTTP 404 for non-existent user.
- API-004: `public_repos` count from API matches UI repository count.
- API-005: `GET /users/{username}/repos` returns list with count equal to `public_repos` (subject to API paging settings).
- API-006: Verify API response time under acceptable threshold (for example < 2s).
- API-007: Verify rate-limit headers exist and are parseable.
- API-008: Validate schema/types for key user fields.
- API-009: Verify repository objects include expected keys (`name`, `html_url`, `stargazers_count`).
- API-010: Validate graceful handling for transient 5xx/network errors with retry policy (framework-level).

## Initial Automated Scope Implemented

- Automated now: **UI+API Happy Path**
  - Search for `swangful`
  - Open profile from search results
  - Verify UI repository count is `17`
  - Verify API `public_repos` count is `17`

- Its me! :D