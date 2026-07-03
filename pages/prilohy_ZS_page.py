from playwright.sync_api import Page
from pytest_playwright.pytest_playwright import page

class PrilohyZS:
    def __init__(self, page: Page):
        self.page = page

    def vyziadat_prilohu(self, dovod: str):
        self.page.get_by_role("button", name="Vyžiadať prílohu").click()
        self.page.get_by_label("Typ prílohy").select_option("3")
        self.page.get_by_role("textbox", name="Dôvod: *").fill(dovod)
        self.page.get_by_role("button", name="Odoslať").click()

    def odvolat_ziadost(self):
        self.page.wait_for_timeout(4000)
        self.page.get_by_role("button", name="Odvolať žiadosť").click()
        self.page.get_by_role("button", name="Áno, odvolať").click()

    def pridat_prilohu(self):
        self.page.get_by_role("link", name="Pridať prílohy").click()
        self.page.get_by_text("Čestné vyhlásenie zákonného zástupcu Nenahrané Nenahrané Nahrané").click()
        
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        self.page.get_by_role("button", name="Odoslať").click()

    def click_on_prejst_na_prihlasky(self):
        self.page.get_by_role("link", name="Prejsť na prihlášky").click()