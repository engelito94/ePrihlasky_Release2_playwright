import os
from datetime import datetime
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment name: local, test, stage, prod",
    )
    parser.addoption(
        "--role",
        action="store",
        default="none",
        help="User role for auth state: none, zz, riaditel",
    )


@pytest.fixture
def credentials():
    return {
        "riaditel_username": os.getenv("EPRIHLASKY_RIADITEL_USERNAME"),
        "riaditel_password": os.getenv("EPRIHLASKY_RIADITEL_PASSWORD"),
        "gmail_primary_user": os.getenv("GMAIL_USERNAME"),
        "gmail_primary_pw": os.getenv("GMAIL_APP_PASSWORD"),
        "gmail_secondary_user": os.getenv("GMAIL_SEC_USERNAME"),
        "gmail_secondary_pw": os.getenv("GMAIL_SEC_APP_PASSWORD"),
    }


@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def role(request) -> str:
    return request.config.getoption("--role")


@pytest.fixture(scope="session")
def base_url(env) -> str:
    urls = {
        "local": os.getenv("EPRIHLASKY_LOCAL_URL", "http://localhost:3000"),
        "test": os.getenv("EPRIHLASKY_TEST_URL", "https://test-eprihlasky.iedu.sk/"),
        "stage": os.getenv("EPRIHLASKY_STAGE_URL", "https://stage.example.com"),
        "prod": os.getenv("EPRIHLASKY_PROD_URL", "https://example.com"),
    }
    return urls[env]


@pytest.fixture(scope="session")
def auth_file(role) -> str | None:
    auth_files = {
        "none": None,
        "zz": "playwright/.auth/ZZ.json",
        "riaditel": "playwright/.auth/riaditel.json",
    }
    return auth_files[role]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url, auth_file):
    context_args = {
        **browser_context_args,
        "base_url": base_url,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }

    if auth_file and Path(auth_file).exists():
        context_args["storage_state"] = auth_file

    return context_args


@pytest.fixture(autouse=True)
def open_base(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    cookies_button = page.get_by_text("Súhlasím", exact=True)

    if cookies_button.is_visible():
        cookies_button.click()

    yield
    


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        page.screenshot(
            path=f"reports/screenshots/{test_name}_{timestamp}.png",
            full_page=True
        )

@pytest.fixture
def email_account_picker(credentials):
    def _pick(current_email: str):
        primary = credentials["gmail_primary_user"]
        secondary = credentials["gmail_secondary_user"]

        if current_email == primary:
            return {
                "new_email": secondary,
                "mail_user": secondary,
                "mail_pw": credentials["gmail_secondary_pw"],
            }

        return {
            "new_email": primary,
            "mail_user": primary,
            "mail_pw": credentials["gmail_primary_pw"],
        }

    return _pick