from playwright.sync_api import Page

class PapierovaPrihlaskaZSSS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.locator("span:has-text('Prihlášky našich žiakov')").click()
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Kolo").select_option("2")
        self.page.wait_for_load_state("networkidle")
        self.page.locator("#btn-vytvorit-prihlasku").click()
    
    def step_1_osobne_udaje(self, meno:str, priezvisko:str, rc:str):
        self.page.get_by_role("radio", name="Áno").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("textbox", name="Meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Rodné priezvisko").fill(priezvisko)
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("slovenska rep")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("deb")
        self.page.get_by_text("Debraď (Košice - okolie)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill("suco")
        self.page.get_by_text("Súčovská").click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("3")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("9")
        self.page.get_by_role("textbox", name="PSČ *").fill("65874")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Pokračovať").click()

    def step_2_SVVP(self):
        self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1").check()
        self.page.locator("#specialneVVP_option_1").check()
        self.page.locator("#mentalnePostihnutie_option_1").check()
        self.page.get_by_role("textbox", name="Poznámka:").fill("ŠVVP")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self):
        self.page.get_by_role("link", name="Pridať odbor").click()
        self.page.get_by_role("textbox", name="Hľadať podľa názvu školy").fill("stredná škola pre AT")
        self.page.locator("#hladat-podla-nazvu-skoly-button").click()
        self.page.get_by_role("button", name="Pridať do prihlášky").first.click()
        self.page.get_by_role("button", name="Pridať odbory a odísť").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_4_ZZ(self):
        self.page.get_by_role("textbox", name="Meno *").fill("Rudolf")
        self.page.get_by_role("textbox", name="Priezvisko *").fill("Brezinoha")
        self.page.get_by_role("textbox", name="Rodné číslo *").fill("760225/6013")
        self.page.get_by_role("textbox", name="E-mail").fill("katalontest987@gmail.com")
        self.page.get_by_role("textbox", name="Telefónne číslo *").fill("+421987654321")
        self.page.wait_for_timeout(500)
        radio = self.page.locator("#zastupca2Radio_option_0")
        radio.click()
        radio.click()
        self.page.locator("#input-zastupca2Meno").fill("Tereza")
        self.page.locator("#input-zastupca2Priezvisko").fill("Brezinohová")
        self.page.locator("#input-zastupca2RodneCislo").fill("765413/0341")
        self.page.locator("#input-zastupca2Email").fill("katalontest789@gmail.com")
        self.page.locator("#input-zastupca2Telefon").fill("+421357951486")
        self.page.get_by_role("radio", name="áno").check()
        self.page.locator("#komunikaciaLenSZZ1 > .checkmark").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_navsteva_ZS(self):
        self.page.locator("#select-rocnikSKSelect").select_option("9")
        self.page.get_by_role("textbox", name="Trieda *").fill("9.A")
        self.page.locator("#select-rokSkolskejDochadzkySKSelect").select_option("9")
        self.page.get_by_role("textbox", name="Názov základnej školy *", exact=True).click()
        self.page.locator("#vyucovaciJazykVZakladnejSkoleSKAutocomplete").get_by_text("slovenský", exact=True).click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_6_znamky(self):
        self.page.locator("#select-hodnotenie-1-1").select_option("29")
        for i in range(18):
            self.page.get_by_role("button", name="Odstrániť").nth(1).click()
        self.page.get_by_text("7. ročník").click()
        self.page.locator("#select-hodnotenie-2-1").select_option("30")
        for i in range(18):
            self.page.get_by_role("button", name="Odstrániť").nth(1).click()
        self.page.get_by_text("8. ročník").click()
        self.page.locator("#select-hodnotenie-3-1").select_option("31")
        for i in range(18):
            self.page.get_by_role("button", name="Odstrániť").nth(1).click()
        self.page.get_by_text("9. ročník").click()
        self.page.locator("#select-hodnotenie-4-1").select_option("29")
        for i in range(18):
            self.page.get_by_role("button", name="Odstrániť").nth(1).click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_7_sutaze(self):
        self.page.get_by_role("button", name="Pridať súťaž").click()
        self.page.get_by_role("textbox", name="Názov súťaže *").fill("Ferova dvanástka")
        self.page.get_by_label("Druh súťaže").select_option("9")
        self.page.get_by_label("Úroveň súťaže").select_option("4")
        self.page.get_by_role("radio", name="Bez umiestnenia").check()
        self.page.get_by_label("Školský rok").select_option("2021/2022")
        self.page.get_by_role("button", name="Pridať", exact=True).click()
        self.page.get_by_role("button", name="Ďalej").click()
        
    def step_8_prilohy(self):
        self.page.locator("span").filter(has_text="Písomné vyhlásenie k podaniam").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_text("Olympiáda / súťaž: Ferova dvanástka Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("#prilohyUploadZone2").get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_role("button", name="Ďalej").click()

    def step_9_ostatne_udaje(self, den:str, mesiac:str, rok:str):
        self.page.get_by_role("textbox", name="Deň").fill(den)
        self.page.get_by_role("textbox", name="Mesiac").fill(mesiac)
        self.page.get_by_role("textbox", name="Rok").fill(rok)
        self.page.get_by_role("textbox", name="Poznámka školy:").fill("(-_-)")
        self.page.get_by_role("button", name="Ďalej").click()

    def click_on_odoslat_prihlasku(self):
        self.page.get_by_role("button", name="Pridať prihlášku").click()
        self.page.wait_for_load_state("load", timeout=15000)

    def najdi_prihlasku(self, meno:str, priezvisko:str):
        self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach").fill(meno + " " + priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()

    def click_on_zobrazit_prihlasku(self):
        self.page.locator("div.riaditel-prihlasky-cell.akcia-cell").locator("button").nth(0).click()

    def click_on_skontrolovana(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Označiť ako skontrolovaná").click()

    def click_on_odoslat_na_SS(self):
        self.page.get_by_role("button", name="Odoslať na stredné školy").click()