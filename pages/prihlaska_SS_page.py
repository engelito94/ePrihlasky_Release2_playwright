from playwright.sync_api import Page, expect


class PrihlaskaSS:
    def __init__(self, page: Page):
        self.page = page
    
    def click_on_vytvorit_prihlasku(self):
        self.page.wait_for_load_state("networkidle") 
        self.page.locator("#btn-vytvorit-prihlasku:visible").click()
        self.page.locator("#modalVytvoritPrihlaskuRadio_option_3").check()
        self.page.locator("button.btn-pridat.govuk-button:visible").click()
        # self.page.get_by_role("button", name="Pridať", exact=True).click()

    def click_on_vytvorit_prihlasku_1_kolo(self):
        self.page.wait_for_load_state("networkidle") 
        self.page.locator("#btn-vytvorit-prihlasku:visible").click()
        self.page.locator("#modalVytvoritPrihlaskuRadio_option_2").check()
        self.page.locator("button.btn-pridat.govuk-button:visible").click()

    def pridat_dieta(self, meno: str, priezvisko: str, rc: str):
        self.page.get_by_role("radio", name="Iný žiak Pridajte dieťa alebo").check()
        self.page.get_by_role("button", name="Pridať žiaka").click()
        self.page.locator("#maDietaRCRadio_option_0").check()
        #self.page.get_by_role("radio", name="Áno").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("textbox", name="Krstné meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Rodné priezvisko").fill(priezvisko)
        self.page.locator("#step-1").get_by_role("button", name="Ďalej").click()
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina").get_by_role("textbox").fill("Slovenská re")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("Myjava")
        self.page.get_by_text("Myjava (Myjava)").click()
        self.page.get_by_role("textbox", name="Krajina *").click()
        self.page.get_by_text("Narcisová", exact=True).click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("4")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("2048")
        self.page.get_by_role("textbox", name="PSČ *").fill("03845")
        self.page.get_by_role("button", name="Pridať dieťa").click()

    def step_1_vyber_ziaka(self):
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1").check()
        self.page.locator("#specialneVVP_option_1").check()
        self.page.locator("#mentalnePostihnutie_option_1").check()
        self.page.get_by_role("textbox", name="Poznámka:").fill("ŠVVP")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self, nazov: str):
        self.page.get_by_role("textbox", name="Názov školy alebo jej adresa").fill(nazov)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.get_by_role("button", name="Stredná škola pre AT Pridať do prihlášky").nth(3).click()
        self.page.get_by_role("button", name="Ďalej").click()
        expect(self.page.locator("#vyber-skoly-message-panel")).to_contain_text("Prihlášku môžete podať len na jeden odbor.")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly_1_kolo(self, nazov: str):
        self.page.get_by_role("textbox", name="Názov školy alebo jej adresa").fill(nazov)
        self.page.get_by_role("button", name="Hľadať").click()
        self.page.get_by_role("button", name="Stredná škola pre AT Pridať do prihlášky").nth(3).click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_label("Termín prijímacej skúšky").select_option("11")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Mám skontrolované").click()

    def step_4_ZZ(self):
        self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je").check()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_ziak_navsteva_skoly(self):
        self.page.get_by_role("radio", name="Zo školy v zahraničí").check()
        self.page.locator("#select-rocnikSelect").select_option("9")
        self.page.locator("#select-rokSkolskejDochadzkySelect").select_option("9")
        self.page.get_by_role("textbox", name="Ročník *").click()
        self.page.get_by_text("francúzsky", exact=True).click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_6_znamky(self):
        self.page.locator("#select-hodnotenie-1-1").select_option("30")
        self.page.locator("#select-hodnotenie-1-2").select_option("1")
        for i in range(17):
            self.page.get_by_role("button", name="Odstrániť").nth(2).click()
        self.page.get_by_text("7. ročník", exact=True).click()
        self.page.locator("#select-hodnotenie-2-1").select_option("31")
        self.page.locator("#select-hodnotenie-2-2").select_option("3")
        for i in range(17):
            self.page.get_by_role("button", name="Odstrániť").nth(2).click()
        self.page.get_by_text("8. ročník", exact=True).click()
        self.page.locator("#select-hodnotenie-3-1").select_option("29")
        self.page.locator("#select-hodnotenie-3-2").select_option("2")
        for i in range(17):
            self.page.get_by_role("button", name="Odstrániť").nth(2).click()
        self.page.get_by_text("9. ročník", exact=True).click()
        self.page.locator("#select-hodnotenie-4-1").select_option("29")
        self.page.locator("#select-hodnotenie-4-2").select_option("1")
        for i in range(17):
            self.page.get_by_role("button", name="Odstrániť").nth(2).click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_7_sutaze(self):
        self.page.get_by_role("button", name="Pridať súťaž").click()
        self.page.get_by_role("textbox", name="Názov súťaže *").fill("Zumba")
        self.page.get_by_label("Druh súťaže").select_option("2")
        self.page.get_by_label("Úroveň súťaže").select_option("6")
        self.page.get_by_role("radio", name="1. miesto").check()
        self.page.get_by_label("Školský rok").select_option("2023/2024")
        self.page.get_by_role("button", name="Pridať", exact=True).click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_8_prilohy(self):
        self.page.get_by_text("Vysvedčenie zo 6. ročníka Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_text("Vysvedčenie zo 7. ročníka Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("#prilohyUploadZone2").get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        
        self.page.get_by_text("Vysvedčenie z 8. ročníka Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("#prilohyUploadZone3").get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_text("Vysvedčenie z 9. ročníka Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("#prilohyUploadZone4").get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_text("Olympiáda / súťaž: Zumba Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("#prilohyUploadZone5").get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        
        self.page.get_by_role("button", name="Ďalej").click()

    def click_on_odoslat_prihlasku(self):
        self.page.locator("#cestnePrehlasenie > .checkmark").click()
        self.page.locator("#suhlasOsobneUdaje > .checkmark").click()
        self.page.get_by_role("button", name="Odoslať prihlášku").click()

    def click_on_potvrdit_odoslanie(self):
        #self.page.get_by_role("button", name="Odoslať prihlášku").nth(1).click()
        self.page.locator("button.btn-confirm.govuk-button.govuk-button__large.last-focusable").click()
        self.page.wait_for_load_state("networkidle")

    def vyhladanie_prihlasky(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle") 
        self.page.get_by_label("Kolo").select_option("2")
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")
        self.page.wait_for_load_state("networkidle") 
        self.page.wait_for_timeout(3000)
        self.page.locator("#fulltext-input").fill(meno + " " + priezvisko)
        self.page.locator("button.govuk-button.govuk-button__basic.button-search:visible").click()

    def click_on_prejst_na_prihlasky(self):
        self.page.get_by_role("button", name="Prejsť na prihlášky").click()