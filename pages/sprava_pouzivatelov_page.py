from playwright.sync_api import Page

class SpravaPouzivatelov:
    def __init__(self, page: Page):
        self.page = page

    def otvor_spravu_pouzivatelov(self):
        self.page.get_by_role("link", name="Správa školy").click()
        self.page.get_by_role("link", name="Správa používateľov").click()

    def click_on_pridat_pouzivatela(self):
        self.page.get_by_role("button", name="Pridať používateľa").click()

    def pridaj_rolu(self, eduid: str, rola: str): 
        self.page.locator("input.govuk-input.autocomplete-input").click()
        self.page.locator(f'div.autocomplete-item[data-value="{eduid}"]').click()
        if rola == "admin":
            self.page.get_by_label("Vyberte rolu").select_option("2")
        self.page.get_by_role("button", name="Pridať").click()

    def otvor_profil(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Rozbaliť profilové menu").click()
        self.page.get_by_role("link", name="Môj profil").click()

    def click_on_odstranit(self):
        self.page.locator("button").filter(has_text="Odstrániť").nth(2).click()
    
    def click_on_potvrdit_odstranenie(self):
        self.page.get_by_role("button", name="Potvrdiť").last.click()
