from playwright.sync_api import Page

class Prijimacky:
    def __init__(self, page: Page):
        self.page = page

    def click_on_menu_prijimacky(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Prijímačky").click()

    def click_on_menu_sprava_prihlasok(self):
        self.page.get_by_role("link", name="Správa prihlášok").click()

    def zmen_kolo_a_odbor(self):
        self.page.get_by_label("Kolo").select_option("2")
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")

    def zmen_odbor_1_kolo(self):
        self.page.get_by_label("Odbor").select_option("fa97e1ee-cf77-4880-853a-5972261cdb4c") 

    def zorad_prihlasky(self):
        self.page.get_by_role("button", name="Zoradiť podľa: Predvolené").click()
        self.page.get_by_role("radio", name="Podľa dátumu podania (od").check()
        self.page.get_by_role("button", name="Zoradiť prihlášky").click()

    def click_on_uprava_prihlasky(self):
        self.page.get_by_role("button", name="Vybrať").first.click()
        self.page.get_by_role("link", name="Upraviť").click()

    def zobraz_prihlasku_detail(self):
        self.page.get_by_role("button", name="Zobraziť").nth(1).click()

    def get_udaje_dietata(self) -> tuple[str, str, str, str]:
        self.page.wait_for_load_state("networkidle")
        pristupovy_kod = self.page.locator("div.pristupovyKod").text_content()
        meno = self.page.locator("#dietaMeno").text_content()
        priezvisko = self.page.locator("#dietaPriezvisko").text_content()
        datum_narodenia = self.page.locator("#dietaDatumNarodenia").text_content()
        return pristupovy_kod, meno, priezvisko, datum_narodenia
    
    def nastavenie_terminu_prijimaciek(self):
        self.page.get_by_role("textbox", name="Deň").fill("12")
        self.page.get_by_role("textbox", name="Mesiac").fill("10")
        self.page.get_by_role("textbox", name="Rok").fill("2026")
        self.page.get_by_role("textbox", name="Hod.").fill("11")
        self.page.get_by_role("textbox", name="Min.").fill("30")
        self.page.get_by_role("textbox", name="Miestnosť").fill("3.E")
        self.page.get_by_role("button", name="Uložiť").click()

    def click_on_akcia_odoslat_pozvanky(self):
        self.page.locator("//body/div[@class='wrapper-full']/div[@class='govuk-width-container']/div[@class='govuk-main-wrapper verejna-zona']/div[@class='sub-container']/div[@class='riaditel-prijimacky-container']/div[@class='fixed-left-column']/div[2]/div[1]/div[1]/span[1]").click()
        self.page.locator("#vykonat-akciu-btn").click()
        self.page.locator("a").filter(has_text="Odoslať pozvánky").last.click()

    def odoslat_pozvanky(self):
        self.page.get_by_role("button", name="Pokračovať").click()
        self.page.get_by_role("textbox", name="Voliteľný text").fill("Dostavte sa na čas a prineste si kružítko.")
        
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("button", name="Vybrať súbor").click()

        file_chooser = fc_info.value
        file_chooser.set_files("./data/Dokument.pdf")

        self.page.get_by_role("button", name="Odoslať").click()

    def click_on_spat_na_prijimacky(self):
        self.page.get_by_role("link", name="Späť na prijímačky").click()

    def click_on_akcia_plny_pocet_bodov(self):
        self.page.locator("//body/div[@class='wrapper-full']/div[@class='govuk-width-container']/div[@class='govuk-main-wrapper verejna-zona']/div[@class='sub-container']/div[@class='riaditel-prijimacky-container']/div[@class='fixed-left-column']/div[2]/div[1]/div[1]/span[1]").click()
        self.page.locator("#vykonat-akciu-btn").click()
        self.page.locator("a").filter(has_text="Odoslať správu o plnom počte bodov").last.click()

    def odoslat_plny_pocet_bodov(self):
        self.page.get_by_role("button", name="Pokračovať").click()
        self.page.get_by_role("button", name="Pokračovať").click()

    def stiahni_pozvanku(self):
        self.page.get_by_role("button", name="Vybrať").first.click()
        with self.page.expect_download() as download_info:
            self.page.locator("a").filter(has_text="Stiahnuť PDF - Pozvánka").last.click()
        download = download_info.value
        download.save_as("data/downloads/pozvankaDownloaded.pdf")

    def stiahni_body(self):
        self.page.get_by_role("button", name="Vybrať").first.click()
        with self.page.expect_download() as download_info:
            self.page.locator("a").filter(has_text="Stiahnuť PDF - Správa o bodoch").last.click()
        download1 = download_info.value
        download1.save_as("data/downloads/bodyDownloaded.pdf")

        