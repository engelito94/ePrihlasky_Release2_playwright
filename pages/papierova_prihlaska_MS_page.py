import re
from playwright.sync_api import Page, expect

class PapierovaPrihlaskaMS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Pridať prihlášku").click()

    def step_1_osobne_udaje(self, meno:str, priezvisko:str, rc:str):
        self.page.get_by_role("radio", name="Áno").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("textbox", name="Meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Rodné priezvisko").fill(priezvisko)
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("slovenská rep")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("Kord")
        self.page.get_by_text("Kordíky (Banská Bystrica)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill("Miksa")
        self.page.get_by_text("Miksáthova").click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("8")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("635")
        self.page.get_by_role("textbox", name="PSČ *").fill("02845")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.get_by_role("radio", name="celodennú výchovu a vzdelá").check()
        self.page.locator("#DPDSVVPRadio_option_1").check()
        self.page.locator("#DPDDietaSNadanimRadio_option_1").check()
        self.page.get_by_role("textbox", name="Deň").fill("1")
        self.page.get_by_role("textbox", name="Mesiac").fill("9")
        self.page.get_by_role("textbox", name="Rok").fill("2026")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self):
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_4_ZZ(self):
        self.page.get_by_role("textbox", name="Meno *").fill("Peter")
        self.page.get_by_role("textbox", name="Priezvisko *").fill("Fodrok")
        self.page.get_by_role("textbox", name="Rodné číslo *").fill("860201/7842")
        self.page.get_by_role("textbox", name="E-mail").fill("katalontest987@gmail.com")
        self.page.get_by_role("textbox", name="Telefónne číslo *").fill("+421905866541")
        self.page.wait_for_timeout(500)
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_prilohy(self):
        self.page.get_by_text("Potvrdenie o zdravotnej spôsobilosti (materská škola) Nenahrané Nenahrané").click()

        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_role("button", name="Ďalej").click()

    def step_6_ostatne_udaje(self, den:str, mesiac:str, rok:str):
        self.page.get_by_role("textbox", name="Deň").fill(den)
        self.page.get_by_role("textbox", name="Mesiac").fill(mesiac)
        self.page.get_by_role("textbox", name="Rok").fill(rok)
        self.page.get_by_role("textbox", name="Poznámka školy:").fill(":)")
        self.page.get_by_role("button", name="Ďalej").click()

    def click_on_odoslat_prihlasku(self):
        self.page.get_by_role("button", name="Pridať prihlášku").click()
        self.page.wait_for_load_state("load", timeout=15000)

    def najdi_prihlasku(self, meno:str, priezvisko:str):
        self.page.get_by_role("textbox", name="Vyhľadávanie v meno,").fill(meno + " " + priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.locator("button").filter(has_text="Zobraziť").first.click()