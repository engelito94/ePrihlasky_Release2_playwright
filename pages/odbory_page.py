from playwright.sync_api import Page

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
    