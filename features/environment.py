from datetime import datetime
import os

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from config.settings import BROWSER, DEFAULT_TIMEOUT_MS, HEADLESS
from utils.config_loader import load_environment
from utils.slack_notifier import SlackNotifier


def before_all(context):
    load_environment()
    context.base_url = os.getenv("BASE_URL", "https://gh-users-search.netlify.app")
    browser_name = os.getenv("BROWSER", BROWSER)
    headless = os.getenv("HEADLESS", str(HEADLESS)).lower() == "true"
    context.test_results = []
    context._pw = sync_playwright().start()
    browser_launcher = getattr(context._pw, browser_name)
    try:
        context.browser = browser_launcher.launch(headless=headless)
    except PlaywrightError as exc:
        if hasattr(context, "_pw"):
            context._pw.stop()
        raise RuntimeError(
            "Playwright browser is not installed. Run: playwright install chromium"
        ) from exc


def before_scenario(context, scenario):
    timeout_ms = int(os.getenv("DEFAULT_TIMEOUT_MS", str(DEFAULT_TIMEOUT_MS)))
    context.context = context.browser.new_context()
    context.page = context.context.new_page()
    context.page.set_default_timeout(timeout_ms)


def after_scenario(context, scenario):
    status = "passed" if scenario.status == "passed" else "failed"
    context.test_results.append({"name": scenario.name, "status": status})

    if hasattr(context, "page"):
        context.page.close()
    if hasattr(context, "context"):
        context.context.close()


def after_all(context):
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "_pw"):
        context._pw.stop()

    notifier = SlackNotifier(os.getenv("SLACK_WEBHOOK_URL", ""))
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    total = len(context.test_results)
    passed = sum(1 for result in context.test_results if result["status"] == "passed")
    failed = total - passed

    message_lines = [
        "*Playwright Behave Test Run*",
        f"Time: {timestamp}",
        f"Total: {total}",
        f"Passed: {passed}",
        f"Failed: {failed}",
    ]

    if failed:
        failed_tests = [result["name"] for result in context.test_results if result["status"] == "failed"]
        message_lines.append(f"Failed tests: {', '.join(failed_tests)}")

    error = notifier.send_message("\n".join(message_lines))
    if error:
        print(error)
