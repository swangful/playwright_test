import os


BASE_URL = os.getenv("BASE_URL", "https://gh-users-search.netlify.app")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("BROWSER", "chromium")
DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")
