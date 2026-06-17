import re
from playwright.sync_api import Page, expect

class SpravaSkoly:
    def __init__(self, page: Page):
        self.page = page
    
    def click_on_menu_sprava_skoly(self) -> None:
        self.page.get_by_role("link", name="Správa školy").click()
    
    def click_on_ulozit_zmeny(self) -> None:
        self.page.get_by_role("button", name="Uložiť zmeny").click()

