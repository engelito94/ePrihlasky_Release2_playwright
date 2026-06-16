from pathlib import Path

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def open_relative(self, path: str):
        self.page.goto(path)

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def type(self, selector: str, value: str):
        self.page.locator(selector).type(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_visible(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    def expect_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str):
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_url_contains(self, text: str):
        expect(self.page).to_have_url(lambda url: text in url)

    def screenshot(self, name: str):
        reports_dir = Path("reports/screenshots")
        reports_dir.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(reports_dir / f"{name}.png"), full_page=True)