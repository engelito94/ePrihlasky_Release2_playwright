from playwright.sync_api import Page

class PapierovaPrihlaskaZS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Pridať prihlášku").click()
        #page.locator("#btn-vytvorit-prihlasku").click()
    
    def step_1_osobne_udaje(self, meno:str, priezvisko:str, rc:str):
        self.page.wait_for_load_state("networkidle")
        #self.page.get_by_role("radio", name="Áno").check()
        self.page.locator("#maDietaRCRadio_option_0").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("textbox", name="Meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Rodné priezvisko").fill(priezvisko)
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("Indi")
        self.page.get_by_text("Indická republika").click()
        self.page.get_by_role("textbox", name="Adresa *").fill("New Dhili, 879/71")
        self.page.locator("#inyMaterinskyJazyk").get_by_role("textbox", name="Miesto narodenia *").fill("an")
        self.page.get_by_text("anglický").click()
        self.page.get_by_role("radio", name="Iná adresa").check()
        self.page.locator("#adresaZAKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("slovenska re")
        self.page.locator("#adresaZAKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaZAObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("vinick")
        self.page.get_by_text("Viničky (Trebišov)").click()
        self.page.get_by_role("textbox", name="Súpisné číslo *").fill("58")
        self.page.get_by_role("textbox", name="PSČ *").fill("11258")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.get_by_role("radio", name="Etická").check()
        self.page.locator("#zsDPDStravovanieRadio_option_0").check()
        self.page.locator("#zsDPDSkolskyKlubRadio_option_1").check()
        self.page.locator("#DPDSVVPRadio_option_1").check()
        self.page.locator("#DPDDietaSNadanimRadio_option_1").check()
        self.page.get_by_role("textbox", name="Poznámka:").fill("ŠVVP")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self):
        pass

    def step_4_ZZ(self):
        self.page.get_by_role("textbox", name="Meno *").fill("Patrik")
        self.page.get_by_role("textbox", name="Priezvisko *").fill("Kvarga")
        self.page.get_by_role("textbox", name="Rodné číslo *").fill("650204/9367")
        self.page.get_by_role("textbox", name="Telefónne číslo *").fill("+421966332557")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Ďalej").click()
        if self.page.get_by_role("textbox", name="Telefónne číslo *").is_visible():
            self.page.get_by_role("button", name="Ďalej").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_navsteva_ZS(self):
        pass

    def step_6_znamky(self):
       pass

    def step_7_sutaze(self):
        pass
        
    def step_8_prilohy(self):
        pass

    def step_9_ostatne_udaje(self, den:str, mesiac:str, rok:str):
        self.page.get_by_role("textbox", name="Deň").fill(den)
        self.page.get_by_role("textbox", name="Mesiac").fill(mesiac)
        self.page.get_by_role("textbox", name="Rok").fill(rok)
        self.page.get_by_role("textbox", name="Poznámka školy:").fill("Poznámka školy.")
        self.page.get_by_role("button", name="Ďalej").click()

    def click_on_odoslat_prihlasku(self):
        self.page.get_by_role("button", name="Pridať prihlášku").click()
        self.page.wait_for_load_state("load", timeout=15000)

    def najdi_prihlasku(self, meno:str, priezvisko:str):
        self.page.get_by_role("textbox", name="Vyhľadávanie v meno,").fill(meno + " " + priezvisko)
        #self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach").fill(meno + " " + priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()

    def click_on_zobrazit_prihlasku(self):
        self.page.locator("div.riaditel-prihlasky-cell.akcia-cell").locator("button").nth(0).click()

    def click_on_skontrolovana(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Označiť ako skontrolovaná").click()

    def click_on_odoslat_na_SS(self):
        self.page.get_by_role("button", name="Odoslať na stredné školy").click()