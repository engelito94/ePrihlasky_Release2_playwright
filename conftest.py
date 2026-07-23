import os
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from playwright.sync_api import Page, expect

expect.set_options(timeout=60000)
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
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)
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
        file_path = f"reports/screenshots/{test_name}_{timestamp}.png"

        screenshot_bytes = page.screenshot(path=file_path, full_page=True)

        allure.attach(
            screenshot_bytes,
            name=f"{test_name}_failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        allure.attach(
            page.content(),
            name=f"{test_name}_page_source",
            attachment_type=allure.attachment_type.HTML
        )

        allure.attach(
            page.url,
            name=f"{test_name}_url",
            attachment_type=allure.attachment_type.TEXT
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

@pytest.fixture
def visual_snapshot(request, page, pytestconfig, browser_name):
    def _compare(name: str, *, threshold: float = 0.1, full_page: bool = True, max_diff_pixels: int = 0):
        snapshot_dir = (
            Path(request.node.fspath).parent.resolve()
            / "__snapshots__"
            / browser_name
            / sys.platform
        )
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        expected_file = snapshot_dir / name
        actual_dir = Path("reports/visual-diffs")
        actual_dir.mkdir(parents=True, exist_ok=True)

        actual_file = actual_dir / f"{request.node.name}_actual.png"
        diff_file = actual_dir / f"{request.node.name}_diff.png"
        expected_copy_file = actual_dir / f"{request.node.name}_expected.png"

        screenshot_bytes = page.screenshot(full_page=full_page, animations="disabled")
        actual_file.write_bytes(screenshot_bytes)

        if pytestconfig.getoption("--update-snapshots"):
            expected_file.write_bytes(screenshot_bytes)
            return

        if not expected_file.exists():
            pytest.fail(f"Snapshot not found: {expected_file}. Use --update-snapshots")

        expected_img = Image.open(expected_file).convert("RGBA")
        actual_img = Image.open(BytesIO(screenshot_bytes)).convert("RGBA")

        if expected_img.size != actual_img.size:
            actual_img.save(actual_file)
            expected_img.save(expected_copy_file)
            pytest.fail(
                f"Image sizes differ. expected={expected_img.size}, actual={actual_img.size}"
            )

        diff_img = Image.new("RGBA", expected_img.size)
        diff_pixels = pixelmatch(
            expected_img,
            actual_img,
            diff_img,
            threshold=threshold
        )

        expected_img.save(expected_copy_file)
        diff_img.save(diff_file)

        allure.attach(expected_file.read_bytes(), name="expected", attachment_type=allure.attachment_type.PNG)
        allure.attach(actual_file.read_bytes(), name="actual", attachment_type=allure.attachment_type.PNG)
        allure.attach(diff_file.read_bytes(), name="diff", attachment_type=allure.attachment_type.PNG)

        assert diff_pixels <= max_diff_pixels, f"Snapshots do not match. Different pixels: {diff_pixels}"

    return _compare