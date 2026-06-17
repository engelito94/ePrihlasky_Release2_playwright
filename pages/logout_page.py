import re
from playwright.sync_api import Page, expect


class LogoutPage:
    def __init__(self, page: Page):
        self.page = page

    def _click_on_menu(self):
        self.page.get_by_role("link", name="Rozbaliť profilové menu").click()
    
    def _click_on_logout(self):
        self.page.get_by_role("link", name="Odhlásiť").click()

    def logout(self):
        self._click_on_menu()
        self._click_on_logout()
