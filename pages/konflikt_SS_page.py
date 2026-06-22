from playwright.sync_api import Page

class KofliktSS:
    def __init__(self, page: Page):
        self.page = page

    def najdi_prihlasku_v_konflikte(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Kolo").select_option("2")
        self.page.get_by_label("Odbor").select_option("2b3813df-fbe6-41ce-be28-0efc6dfaca83")
        self.page.get_by_role("button", name="Zoradiť podľa: Predvolené").click()
        self.page.get_by_role("radio", name="Podľa dátumu podania (od").check()
        self.page.get_by_role("button", name="Zoradiť prihlášky").click()
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Zobraziť").nth(1).click()
        self.page.wait_for_load_state("networkidle")

    def click_on_vyzva_na_vyriesenie_konfliktu(self):
        self.page.get_by_role("button", name="Vyzvať na riešenie konfliktu").click()

    def click_on_odoslat_vyzvu(self, text: str):
        self.page.get_by_role("textbox", name="Sprievodná správa:").fill(text)
        self.page.get_by_role("button", name="Odoslať výzvu").click()

    def click_on_vyriesit_konflikt(self):
        self.page.locator("#btn-vyriesit-konflikt").click()

    def click_on_odoslat_konfikt(self, text: str):
        self.page.locator("#textarea-sprievodnaSpravaTextarea").fill(text)
        self.page.locator("button.btn-vyriesit-konflikt.govuk-button.govuk-button__basic.last-focusable").click()

