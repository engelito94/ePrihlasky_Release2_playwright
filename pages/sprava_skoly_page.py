from playwright.sync_api import Page
from pages.base_page import BasePage


class SpravaSkoly(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def click_on_menu_sprava_skoly(self) -> None:
        self._safe_click(
            self.page.get_by_role("link", name="Správa školy"),
            "Správa školy"
        )

    def click_on_ulozit_zmeny(self) -> None:
        self._safe_click(
            self.page.get_by_role("button", name="Uložiť zmeny"),
            "Uložiť zmeny"
        )