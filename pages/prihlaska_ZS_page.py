from playwright.sync_api import Page
from pytest_playwright.pytest_playwright import page

class PrihlaskaZS:
    def __init__(self, page: Page):
        self.page = page
    
    def pridanie_prihlasky(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_text("Vytvoriť prihlášku").first.click()
        self.page.get_by_role("radio", name="Základná škola Prihlášku môž").check()
        self.page.get_by_role("button", name="Pridať", exact=True).click()

    def step_1_pridat_dieta(self, meno: str, priezvisko: str, rodne_cislo: str):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("radio", name="Iné dieťa Pridajte dieťa").check()
        self.page.get_by_role("button", name="Pridať dieťa").click()
        #self.page.get_by_role("radio", name="Áno").check()
        self.page.locator("#maDietaRCRadio_option_0").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rodne_cislo)
        self.page.get_by_role("textbox", name="Krstné meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.locator("#step-1").get_by_role("button", name="Ďalej").click()
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina").get_by_role("textbox").fill("slovenska re")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("Brusno")
        self.page.get_by_text("Brusno (Banská Bystrica)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill("cibulk")
        self.page.get_by_text("Cibulková").click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("8")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("63")
        self.page.get_by_role("textbox", name="PSČ *").fill("03687")
        self.page.locator("#step-2").get_by_role("button", name="Pridať dieťa").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.get_by_role("radio", name="Náboženská").check()
        self.page.get_by_role("radio", name="Rímskokatolícka").check()
        self.page.locator("#zsDPDStravovanieRadio_option_0").check()
        self.page.locator("#zsDPDSkolskyKlubRadio_option_0").check()
        self.page.locator("#DPDSVVPRadio_option_1").check()
        self.page.locator("#DPDDietaSNadanimRadio_option_1").check()
        self.page.get_by_role("textbox", name="Poznámka:").fill("ŠVVP")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self, nazov_skoly: str):
        self.page.get_by_role("radio", name="Hľadať podľa názvu školy").check()
        self.page.get_by_role("textbox", name="Názov školy alebo jej adresa *").fill(nazov_skoly)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.get_by_role("button", name="Základná škola pre AT Pridať do prihlášky").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Mám skontrolované").click()

    def step_4_ZZ(self):
        self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je").check()
        self.page.get_by_role("button", name="Ďalej").click()
    
    def step_5_prilohy(self):
        self.page.get_by_role("button", name="Ďalej").click()