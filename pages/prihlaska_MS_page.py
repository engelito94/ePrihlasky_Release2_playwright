from playwright.sync_api import Page

class PrihlaskaMS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_vytvorit_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_text("Vytvoriť prihlášku").first.click()
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("radio", name="Materská škola Prihlášku môž").check()
        self.page.get_by_role("button", name="Pridať", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def step_1_pridat_dieta(self, meno: str, priezvisko: str, rc: str):
        self.page.get_by_role("radio", name="Iné dieťa Pridajte dieťa").check()
        self.page.get_by_role("button", name="Pridať dieťa").click()
        self.page.wait_for_load_state("networkidle")
        self.page.locator("#maDietaRCRadio_option_0").check()
        #page.get_by_role("radio", name="Áno").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("textbox", name="Krstné meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.locator("#step-1").get_by_role("button", name="Ďalej").click()
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina").get_by_role("textbox").fill("Slovenska re")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("bobo")
        self.page.get_by_text("Bobot (Trenčín)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill("debra")
        self.page.get_by_text("Debraďská").click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("999")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("21")
        self.page.get_by_role("textbox", name="PSČ *").fill("54231")
        self.page.locator("#step-2").get_by_role("button", name="Pridať dieťa").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.get_by_role("radio", name="Celodennú výchovu a vzdelá").check()
        self.page.locator("#DPDSVVPRadio_option_1").check()
        self.page.locator("#DPDDietaSNadanimRadio_option_1").check()
        self.page.get_by_role("textbox", name="Deň").fill("7")
        self.page.get_by_role("textbox", name="Mesiac").fill("9")
        self.page.get_by_role("textbox", name="Rok").fill("2026")
        self.page.get_by_role("textbox", name="Poznámka:").fill("ŠVVP")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self, nazov: str):
        self.page.get_by_role("radio", name="Hľadať podľa názvu školy").check()
        self.page.get_by_role("textbox", name="Názov školy alebo jej adresa *").fill(nazov)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.get_by_role("button", name="Materská škola pre AT Pridať do prihlášky").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Mám skontrolované").click()

    def step_4_ZZ(self):
        self.page.get_by_role("textbox", name="Meno *").fill("Fero")
        self.page.get_by_role("textbox", name="Priezvisko *").fill("Bartoš")
        self.page.get_by_role("textbox", name="Rodné číslo *").fill("860224/7005")
        self.page.get_by_role("textbox", name="E-mail *").fill("mail@tst.net")
        self.page.locator("#input-zastupca2Telefon").fill("+421954856321")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_prilohy(self):
        self.page.get_by_text("Potvrdenie o zdravotnej spôsobilosti (materská škola) Nenahrané Nenahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_role("button", name="Ďalej").click()

    def odoslat_prihlasku_MS(self):
        self.  page.locator("#cestnePrehlasenie > .checkmark").click()
        self.page.locator("#suhlasOsobneUdaje > .checkmark").click()
        self.page.get_by_role("button", name="Odoslať prihlášku").click()
        self.page.get_by_role("button", name="Odoslať prihlášku").nth(1).click()

    def vyhladaj_prihlasku(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")
        #self.page.get_by_role("textbox", name="Vyhľadávanie v meno,").fill(meno + " " + priezvisko)
        self.page.locator("#fulltext-input").fill(meno + " " + priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.locator("button").filter(has_text="Zobraziť").first.click()
        self.page.wait_for_load_state("networkidle")