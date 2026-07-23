from pathlib import Path
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _safe_click(self, locator: Locator, nazov_prvku: str, timeout: int = 60000, screenshot_on_error: bool = True):
        try:
            expect(locator, f'Prvok "{nazov_prvku}" nie je viditeľný pred kliknutím.').to_be_visible(timeout=timeout)
            locator.click(timeout=timeout)
        except Exception as e:
            if screenshot_on_error:
                self.screenshot(f"error_click_{self._sanitize_filename(nazov_prvku)}")
            raise AssertionError(f'Kliknutie na prvok "{nazov_prvku}" nebolo úspešné: {e}')

    def _safe_fill(self, locator: Locator, hodnota: str, nazov_prvku: str, timeout: int = 60000, screenshot_on_error: bool = True):
        try:
            expect(locator, f'Pole "{nazov_prvku}" nie je viditeľné pred vyplnením.').to_be_visible(timeout=timeout)
            locator.fill(hodnota, timeout=timeout)
        except Exception as e:
            if screenshot_on_error:
                self.screenshot(f"error_fill_{self._sanitize_filename(nazov_prvku)}")
            raise AssertionError(f'Vyplnenie poľa "{nazov_prvku}" hodnotou "{hodnota}" nebolo úspešné: {e}')

    def _safe_select(self, locator: Locator, hodnota: str, nazov_prvku: str, timeout: int = 60000, screenshot_on_error: bool = True):
        try:
            expect(locator, f'Pole "{nazov_prvku}" nie je viditeľné pred výberom hodnoty.').to_be_visible(timeout=timeout)
            locator.select_option(hodnota, timeout=timeout)
        except Exception as e:
            if screenshot_on_error:
                self.screenshot(f"error_select_{self._sanitize_filename(nazov_prvku)}")
            raise AssertionError(f'Výber hodnoty "{hodnota}" v poli "{nazov_prvku}" nebol úspešný: {e}')

    def _safe_check(self, locator: Locator, nazov_prvku: str, timeout: int = 60000, screenshot_on_error: bool = True):
        try:
            expect(locator, f'Prvok "{nazov_prvku}" nie je viditeľný pred označením.').to_be_visible(timeout=timeout)
            locator.check(timeout=timeout)
        except Exception as e:
            if screenshot_on_error:
                self.screenshot(f"error_check_{self._sanitize_filename(nazov_prvku)}")
            raise AssertionError(f'Označenie prvku "{nazov_prvku}" nebolo úspešné: {e}')

    def _safe_set_files(self, locator: Locator, cesta_k_suboru: str, nazov_prvku: str, timeout: int = 60000, screenshot_on_error: bool = True):
        try:
            expect(locator, f'Upload prvok "{nazov_prvku}" nie je viditeľný pred nahraním súboru.').to_be_visible(timeout=timeout)
            locator.set_input_files(cesta_k_suboru, timeout=timeout)
        except Exception as e:
            if screenshot_on_error:
                self.screenshot(f"error_upload_{self._sanitize_filename(nazov_prvku)}")
            raise AssertionError(f'Nahratie súboru "{cesta_k_suboru}" do prvku "{nazov_prvku}" nebolo úspešné: {e}')

    def _expect_visible(self, locator: Locator, message: str, timeout: int = 60000):
        expect(locator, message).to_be_visible(timeout=timeout)

    def _expect_contains_text(self, locator: Locator, text: str, message: str, timeout: int = 60000):
        expect(locator, message).to_contain_text(text, timeout=timeout)

    def _expect_exact_text(self, locator: Locator, text: str, message: str, timeout: int = 60000):
        expect(locator, message).to_have_text(text, timeout=timeout)

    def _expect_value(self, locator: Locator, value: str, message: str, timeout: int = 60000):
        expect(locator, message).to_have_value(value, timeout=timeout)

    def _sanitize_filename(self, name: str) -> str:
        return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name).strip("_").lower()

    def screenshot(self, name: str):
        reports_dir = Path("reports/screenshots")
        reports_dir.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(reports_dir / f"{name}.png"), full_page=True)