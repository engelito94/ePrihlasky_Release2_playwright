from playwright.sync_api import Page


class ProfilZZ:
    def __init__(self, page: Page):
        self.page = page

    def otvorit_profil(self):
        self.page.get_by_role("link", name="Rozbaliť profilové menu").click()
        self.page.get_by_role("link", name="Môj profil").click()
        self.page.wait_for_load_state("networkidle")

    def zmen_tel_cislo(self, cislo : str):
        self.page.get_by_role("link", name="Upraviť údaje").click()
        self.page.get_by_role("textbox", name="Telefónne číslo *").fill(cislo)

    def click_on_ulozit_zmeny(self):
        self.page.locator("button.btn-ulozit.govuk-button.govuk-button__large.disabled").click()

    def zmenit_mail(self, mail: str):
        self.page.get_by_role("button", name="Zmeniť e-mail").click()
        self.page.get_by_role("textbox", name="Vaša nová emailová adresa *").fill(mail)
        self.page.get_by_role("button", name="Zmeniť email").click()

    def overit_kod_mailu(self, kod: str):
        self. page.get_by_role("textbox", name="Overovací kód *").fill(kod)
        self.page.get_by_role("button", name="Overiť").click()

    def zmenit_adresu(self, krajina: str, mesto: str, ulica: str, scislo: str, ocislo: str, psc: str):
        self.page.get_by_role("radio", name="Iná korešpondenčná adresa").check()
        self.page.locator("#adresaTPKrajina").get_by_role("textbox").fill(krajina)
        self.page.get_by_text("Slovenská republika", exact=True).click()
        self.page.locator("#adresaTPObec").get_by_role("textbox").fill(mesto)
        if  mesto == "semero":
            self.page.get_by_text("Semerovo (Nové Zámky)").click()
        else:
            self.page.get_by_text("Trebatice (Piešťany)").click()
        self.page.get_by_role("textbox", name="Krajina *").fill(ulica)
        if  ulica == "kuri":
            self.page.get_by_text("Kúria").click()
        else:
            self.page.get_by_text("Záštepy", exact=True).click()
        
        if scislo == "32":
            self.page.get_by_role("textbox", name="Súpisné číslo").fill(scislo)
        self.page.get_by_role("textbox", name="Orientačné číslo *").fill(ocislo)
        self.page.get_by_role("textbox", name="PSČ *").fill(psc)
        self.page.locator("#ulozit-adresu").click()