import random
import re
import string
import time
from playwright.sync_api import Playwright


class MailTmClient:
    BASE_URL = "https://api.mail.tm"

    def __init__(self, playwright: Playwright):
        self.api = playwright.request.new_context(
            base_url=self.BASE_URL,
            extra_http_headers={"Content-Type": "application/json"}
        )

    def _random_string(self, length: int = 10) -> str:
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def create_temp_mailbox(self) -> tuple[str, str]:
        domains_response = self.api.get("/domains")
        assert domains_response.ok, f"Domains call failed: {domains_response.status}"
        domains_json = domains_response.json()
        domain = domains_json["hydra:member"][0]["domain"]

        email = f"{self._random_string()}@{domain}".lower()
        password = f"Pw{self._random_string(10)}1!"

        create_response = self.api.post(
            "/accounts",
            data={"address": email, "password": password}
        )
        assert create_response.status == 201, create_response.text()

        token_response = self.api.post(
            "/token",
            data={"address": email, "password": password}
        )
        assert token_response.status == 200, token_response.text()

        token = token_response.json()["token"]
        return email, token

    def wait_for_registration_link(self, token: str, timeout_seconds: int = 60) -> str:
        deadline = time.time() + timeout_seconds
        auth_api = self.api

        while time.time() < deadline:
            messages_response = auth_api.get(
                "/messages",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert messages_response.status == 200, messages_response.text()
            messages_json = messages_response.json()
            messages = messages_json.get("hydra:member", [])

            if messages:
                message_id = messages[0]["id"]
                message_response = auth_api.get(
                    f"/messages/{message_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                assert message_response.status == 200, message_response.text()
                message_json = message_response.json()

                text = message_json.get("text", "") or ""
                match = re.search(r"https?://\S+", text)
                if match:
                    return match.group(0).rstrip("].,>)")

            time.sleep(5)

        raise AssertionError("Registration email did not arrive in time")

    def dispose(self):
        self.api.dispose()