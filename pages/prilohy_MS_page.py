from playwright.sync_api import Page

class PrilohyMS:
    def __init__(self, page: Page):
        self.page = page

    def vyziadanie_prilohy_MS(self):
        self.page.wait_for_timeout(2000)
        self.page.get_by_role("button", name="Vyžiadať prílohu").click()
        self.page.get_by_label("Typ prílohy").select_option("1")
        self.page.get_by_role("textbox", name="Dôvod: *").fill("Odvolanie prílohy.")
        self.page.get_by_role("button", name="Odoslať").click()

    def odvolanie_prilohy_MS(self):
        self.page.wait_for_timeout(3000)
        self.page.get_by_role("button", name="Odvolať žiadosť").click()
        self.page.get_by_role("button", name="Áno, odvolať").click()

    def pridat_prilohu_MS(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Pridať prílohy").click()
        self.page.locator("span").filter(has_text="add").first.click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        self.page.get_by_role("button", name="Odoslať").click()

    