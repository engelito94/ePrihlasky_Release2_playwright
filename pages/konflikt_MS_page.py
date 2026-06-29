import re
from playwright.sync_api import Page

class konfliktMS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_vyzva_na_vyriesenie_konfliktu(self):
        self.page.get_by_role("button", name="Vyzvať na riešenie konfliktu").click()

    def odoslat_vyzvu_na_vyriesenie_konfliktu(self):
        self.page.get_by_role("textbox", name="Sprievodná správa: *").fill("Výzva na vyriešenie konfliktu.")
        self.page.get_by_role("button", name="Odoslať výzvu").click()

    def click_on_vyriesenie_konfliktu(self):
        self.page.get_by_role("button", name="Vyriešiť konflikt").click()

    def odoslat_vyriesenie_konfliktu(self, text: str):
        self.page.get_by_role("textbox", name="Sprievodná správa: *").fill(text)
        self.page.locator("button").filter(has_text=re.compile(r"^Vyriešiť konflikt$")).click()