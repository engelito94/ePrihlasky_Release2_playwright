from playwright.sync_api import Page
import re

class Odbory:
    def __init__(self, page: Page):
        self.page = page

    def click_on_menu_odbory(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Odbory a kritériá").click()

    def click_on_otvorit_odbor(self):
        self.page.get_by_role("button", name="Otvoriť odbor pre 2. kolo").click()

    def vyber_odbor_kapacitu(self):
        self.page.get_by_label("Odbor pre 2. kolo").select_option("6565e543-a930-4141-ac45-4a96433cd5f4")
        self.page.get_by_role("textbox", name="Kapacita odboru pre 2. kolo *").fill("100")
        self.page.get_by_role("button", name="Pridať").click()

    def click_on_zverejnit_odbor(self):
        self.page.get_by_role("button", name="Zverejniť odbory pre 2. kolo").click()

    def odstran_odbor(self):
        self.page.get_by_role("button", name="Zrušiť").click()
        self.page.get_by_role("button", name="Odstrániť").click()

    def pridaj_odbor_1_kolo(self):
        self.page.get_by_role("link", name="Odbory a kritériá").click()
        self.page.locator("#btnPridatOdbor").click()
        self.page.get_by_text("cestovný ruch 6314N00 •").click()
        self.page.locator(".checkmark").first.click()
        self.page.locator(".checkmark").first.click()
        self.page.get_by_role("button", name="Pridať odbor/y").click()

    def aktualizuj_odbory_1_kolo(self):
        self.page.get_by_role("button", name="Upraviť").click()
        self.page.get_by_role("textbox", name="Kapacita odboru *").fill("55")
        self.page.locator("div:nth-child(6) > .checkmark").first.click()
        self.page.get_by_text("Žiaci 8. ročníka").click()
        self.page.get_by_label("Dĺžka štúdia").select_option("20")
        self.page.get_by_label("Forma štúdia").select_option("101")
        self.page.locator("#modalUpravitOdborDualneVzdelavania > .checkmark").click()
        self.page.get_by_role("textbox", name="IČO zamestnávateľa").fill("31385401")
        self.page.get_by_role("link", name="Pridať").click()
        self.page.get_by_role("textbox", name="Kapacita pre duálne vzdelá").fill("12")
        self.page.locator("#modalUpravitOdborPrijimaciaSkuska > .checkmark").click()
        self.page.locator("#modalUpravitOdborPrijimaciaSkuskaCheckboxList > .govuk-form-group.checkbox-list-control > .govuk-fieldset > .govuk-checkboxes > div > .checkmark").first.click()
        self.page.locator("#modalUpravitOdborPrijimaciaSkuskaCheckboxList > .govuk-form-group.checkbox-list-control > .govuk-fieldset > .govuk-checkboxes > div:nth-child(3) > .checkmark").click()
        self.page.get_by_role("button", name="Uložiť zmeny").click()
    
    def odstran_odbor_1_kolo(self):
        self.page.get_by_role("button", name="Odstrániť").click()
        self.page.locator("button").filter(has_text=re.compile(r"^Odstrániť$")).click()