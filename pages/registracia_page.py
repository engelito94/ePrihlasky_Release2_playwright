from playwright.sync_api import Page
from pages.base_page import BasePage


class Registracia(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def click_on_registracia(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.get_by_role("link", name="Registrácia"),
            "Registrácia"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Registrácia cez registračný"),
            "Registrácia cez registračný formulár"
        )

    def vypln_registracny_formular(
        self,
        mail: str,
        heslo: str,
        meno: str,
        priezvisko: str,
        rc: str,
        op: str
    ):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Zopakujte e-mail ("),
            mail,
            "Zopakujte e-mail"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="E-mail (prihlasovacie meno) *", exact=True),
            mail,
            "E-mail (prihlasovacie meno)"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Heslo *", exact=True),
            heslo,
            "Heslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Zopakujte heslo *"),
            heslo,
            "Zopakujte heslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Meno *"),
            meno,
            "Meno"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            priezvisko,
            "Priezvisko"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Číslo občianskeho preukazu *"),
            op,
            "Číslo občianskeho preukazu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            rc,
            "Rodné číslo"
        )
        self._safe_check(
            self.page.locator("#suhlas-input"),
            "Súhlas so spracovaním údajov"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zaregistrovať"),
            "Zaregistrovať"
        )