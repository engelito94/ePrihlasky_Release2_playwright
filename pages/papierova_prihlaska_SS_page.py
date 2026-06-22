from playwright.sync_api import Page

class PapierovaPrihlaskaSS:
    def __init__(self, page: Page):
        self.page = page

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Kolo").select_option("2")
        self.page.wait_for_load_state("networkidle")
        self.page.locator("#btn-vytvorit-prihlasku").click()
    
    def step_1_osobne_udaje(self, meno:str, priezvisko:str, rc:str):
        self.page.get_by_role("radio", name="Áno").check()
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.get_by_role("button", name="Ďalej").click()

        button = self.page.locator("button.btn-confirm.govuk-button.govuk-button__large.last-focusable")
        if button.is_visible:
            button.click()
            
        self.page.get_by_role("textbox", name="Meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Rodné priezvisko").fill(priezvisko)
        self.page.locator("#input-miestoNarodenia").fill("Slovensko")
        self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("slovenska rep")
        self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input").fill("pali")
        self.page.get_by_text("Palín (Michalovce)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill("korce")
        self.page.get_by_text("Korčekova").click()
        self.page.get_by_role("textbox", name="Súpisné číslo").fill("12")
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill("45")
        self.page.get_by_role("textbox", name="PSČ *").fill("89516")
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_2_SVVP(self):
        self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1").check()
        self.page.locator("#specialneVVP_option_1").check()
        self.page.locator("#mentalnePostihnutie_option_1").check()
        self.page.get_by_role("textbox", name="Poznámka:").fill("-_-")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_3_vyber_skoly(self):
        self.page.get_by_role("link", name="Pridať odbor mojej školy").click()
        self.page.get_by_role("button", name="Pridať do prihlášky").first.click()
        self.page.get_by_role("button", name="Pridať odbory a odísť").click()
        self.page.get_by_role("button", name="Ďalej").click()
        self.page.get_by_role("button", name="Ďalej").click()

    def step_4_ZZ(self):
        self.page.get_by_role("textbox", name="Meno *").fill("Demeter")
        self.page.get_by_role("textbox", name="Priezvisko *").fill("Varga")
        self.page.get_by_role("textbox", name="Rodné číslo *").fill("840303/7269")
        self.page.get_by_role("textbox", name="E-mail").fill("katalontest987@gmail.com")
        self.page.get_by_role("textbox", name="Telefónne číslo *").fill("+421963258741")
        self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je").check()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("button", name="Ďalej").click()

    def step_5_navsteva_ZS(self):
        self.page.get_by_role("textbox", name="EDUID základnej školy *").fill("910021625")
        self.page.get_by_text("Informácie o základnej škole Vyplňte dodatočné informácie o základnej škole.").click()
        self.page.locator("#select-rocnikSKSelect").select_option("9")
        self.page.get_by_role("textbox", name="Trieda *").fill("9.A")
        self.page.locator("#select-rokSkolskejDochadzkySKSelect").select_option("9")
        self.page.get_by_role("textbox", name="Názov základnej školy *", exact=True).fill("slovenský")
        self.page.locator("#vyucovaciJazykVZakladnejSkoleSKAutocomplete").get_by_text("slovenský", exact=True).click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("button", name="Ďalej").click()
        #self.page.get_by_role("button", name="Ďalej").click()

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
        self.page.get_by_role("textbox", name="Názov súťaže *").fill("Preteky v kosení")
        self.page.get_by_label("Druh súťaže").select_option("3")
        self.page.get_by_label("Úroveň súťaže").select_option("3")
        self.page.get_by_role("radio", name="2. miesto").check()
        self.page.get_by_label("Školský rok").select_option("2024/2025")
        self.page.get_by_role("button", name="Pridať", exact=True).click()
        self.page.get_by_role("button", name="Ďalej").click()
        
    def step_8_prilohy(self):
        self.page.get_by_text("Olympiáda / súťaž: Preteky v kosení Nenahrané Nenahrané Nahrané").click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("link", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")
        self.page.get_by_role("button", name="Ďalej").click()

    def step_9_ostatne_udaje(self, den:str, mesiac:str, rok:str):
        self.page.get_by_role("textbox", name="Deň").fill(den)
        self.page.get_by_role("textbox", name="Mesiac").fill(mesiac)
        self.page.get_by_role("textbox", name="Rok").fill(rok)
        self.page.get_by_role("textbox", name="Poznámka školy:").fill("*-*")
        self.page.get_by_role("button", name="Ďalej").click()

    def click_on_odoslat_prihlasku(self):
        self.page.get_by_role("button", name="Pridať prihlášku").click()
        self.page.wait_for_load_state("load", timeout=15000)

    def najdi_prihlasku(self, meno:str, priezvisko:str):
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")
        self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach").fill(meno + " " + priezvisko)
        self.page.get_by_role("button", name="Hľadať").click()

    def click_on_zobrazit_prihlasku(self):
        self.page.locator("div.riaditel-prihlasky-cell.akcia-cell").locator("button").nth(0).click()