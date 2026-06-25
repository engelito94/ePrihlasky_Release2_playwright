import re
from playwright.sync_api import Page, expect


class ProfilPage:
    def __init__(self, page: Page):
        self.page = page

    def _open_profil(self):
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("link", name="Rozbaliť profilové menu").click()
        self.page.get_by_role("link", name="Môj profil").click()
        self.page.wait_for_load_state("networkidle")
    
    def _change_phone_number(self, cislo : str):
        self.page.get_by_role("textbox", name="Telefónne číslo").fill(cislo)
        self.page.get_by_role("button", name="Uložiť zmeny").click()

    def click_on_profil(self):
        self._open_profil()

    def click_on_upravit_udaje(self):
        self.page.get_by_role("link", name="Upraviť údaje").click()

    def change_tel_cislo(self, cislo : str):
        self._change_phone_number(cislo)

    def change_email(self, mail:str):
        self.page.get_by_role("textbox", name="Vaša nová emailová adresa *").fill(mail)
        self.page.get_by_role("button", name="Zmeniť email").click()

    def load_kod(self, kod : str):
        self.page.get_by_role("textbox", name="Overovací kód *").fill(kod)
        self.page.get_by_role("button", name="Overiť").click()
        self.page.wait_for_load_state("networkidle")

    def get_email_riaditela(self) -> str:
        return self.page.locator("#profil-riaditel-mail").text_content()