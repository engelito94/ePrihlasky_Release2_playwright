from playwright.sync_api import Page

class Registracia:
    def __init__(self, page: Page):
        self.page = page

    def click_on_registracia(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Registrácia").click()
        self.page.get_by_role("link", name="Registrácia cez registračný").click()

    def vypln_registracny_formular(self, mail: str, heslo: str, meno: str, priezvisko: str, rc:str, op: str):
        self.page.get_by_role("textbox", name="Zopakujte e-mail (").fill(mail)
        self.page.get_by_role("textbox", name="E-mail (prihlasovacie meno) *", exact=True).fill(mail)
        self.page.get_by_role("textbox", name="Heslo *", exact=True).fill(heslo)
        self.page.get_by_role("textbox", name="Zopakujte heslo *").fill(heslo)
        self.page.get_by_role("textbox", name="Meno *").fill(meno)
        self.page.get_by_role("textbox", name="Priezvisko *").fill(priezvisko)
        self.page.get_by_role("textbox", name="Číslo občianskeho preukazu *").fill(op)
        self.page.get_by_role("textbox", name="Rodné číslo *").fill(rc)
        self.page.locator("#suhlas-input").check()
        self.page.get_by_role("button", name="Zaregistrovať").click()