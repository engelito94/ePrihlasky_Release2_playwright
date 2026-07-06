from playwright.sync_api import Page

class PrilohySS:
    def __init__(self, page: Page):
        self.page = page

    def najdi_poslednu_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Kolo").select_option("2")
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")
        self.page.get_by_role("button", name="Zoradiť podľa: Predvolené").click()
        self.page.get_by_role("radio", name="Podľa dátumu podania (od").check()
        self.page.get_by_role("button", name="Zoradiť prihlášky").click()
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Zobraziť").nth(1).click()
        self.page.wait_for_load_state("networkidle")

    def vyziadaj_prilohu_na_poslednej_prihlaske(self):
        self.page.get_by_role("button", name="Vyžiadať prílohu").click()
        self.page.get_by_label("Typ prílohy").select_option("3")
        self.page.get_by_role("textbox", name="Dôvod: *").fill("Žiadosť o doplnenie prílohy.")
        self.page.get_by_role("button", name="Odoslať").click()

    def odvolanie_ziadosti(self):
        self.page.wait_for_timeout(5000)  #pevný tiemout, kvôli čakaniu na e-mail k odvolaniu
        self.page.get_by_role("button", name="Odvolať žiadosť").click()
        self.page.get_by_role("button", name="Áno, odvolať").click()

    def nahrat_prilohu(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Pridať prílohy").click()
        self.page.get_by_text("Čestné vyhlásenie zákonného zástupcu Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        self.page.get_by_role("button", name="Odoslať").click()

    def click_on_prejst_na_prihlasky(self):
        self.page.get_by_role("link", name="Prejsť na prihlášky").click()

    def najdi_prihlasku_po_nahrati_prilohy(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Kolo").select_option("2")
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")
        self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach").dblclick()
        self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach").fill(meno+" "+priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.get_by_role("button", name="Zobraziť").nth(1).click()
        self.page.wait_for_load_state("networkidle")