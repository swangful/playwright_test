import json
import urllib.error
import urllib.request
from typing import Optional


class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, message: str) -> Optional[str]:
        if not self.webhook_url:
            return "Slack webhook URL not configured."

        payload = {"text": message}
        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status >= 300:
                    return f"Slack webhook call failed with HTTP {response.status}."
        except urllib.error.URLError as exc:
            return f"Slack webhook call failed: {exc}"

        return None
