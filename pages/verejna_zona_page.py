import re
from playwright.sync_api import Page, expect


class VerejnaZona:
    def __init__(self, page: Page):
        self.page = page

    def _click_on_najst_skolu(self) -> None:
        self.page.locator("#header-navigation").get_by_role("link", name="Nájsť školu").click()
        self.page.wait_for_load_state("load")
    
    def _hladat_podla_nazvu(self, nazov: str) -> None:
        self.page.get_by_role("radio", name="Hľadať podľa názvu školy").check()
        self.page.get_by_role("textbox", name="Názov školy alebo jej adresa *").fill(nazov)
        self.page.get_by_role("button", name="Hľadať").click()

    def _hladat_SS(self, nazov: str) -> None:
        self.page.locator("#fulltext-input-SS").fill(nazov)
        self.page.locator("#fulltext-input-SS-button").click()

    def _click_info(self, eduid: str) -> None:
        self.page.locator(f'#skola-{eduid}').get_by_role("link", name="Viac informácií o škole").click()

    def _click_typ_skoly(self, typ: str) -> None:
        self.page.wait_for_timeout(1000)
        item = self.page.locator(f'li:has-text("{typ}")')
        item.click()
        classes = item.get_attribute("class") or ""

        if "navigation-item-active" not in classes:
            item.click()

    def vyhladaj_skolu(self, nazov: str, eduid: str, typ: str):
        self._click_on_najst_skolu()
        self._click_typ_skoly(typ)
        if (typ == "Stredné školy"):
            self._hladat_SS(nazov)
        else:
            self._hladat_podla_nazvu(nazov)
        self._click_info(eduid)

    def click_on_profil_skoly(self) -> None:
        self.page.get_by_role("button", name="Zobraziť profil školy").click()
    
    