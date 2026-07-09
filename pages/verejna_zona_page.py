from playwright.sync_api import Page
from pages.base_page import BasePage


class VerejnaZona(BasePage):
    TYP_SS = "Stredné školy"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_on_najst_skolu(self) -> None:
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.locator("#header-navigation").get_by_role("link", name="Nájsť školu"),
            "Nájsť školu"
        )
        self.page.wait_for_load_state("load")

    def _hladat_podla_nazvu(self, nazov: str) -> None:
        self._safe_check(
            self.page.get_by_role("radio", name="Hľadať podľa názvu školy"),
            "Hľadať podľa názvu školy"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Názov školy alebo jej adresa *"),
            nazov,
            "Názov školy alebo jej adresa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self.page.wait_for_load_state("networkidle")

    def _hladat_SS(self, nazov: str) -> None:
        self._safe_fill(
            self.page.locator("#fulltext-input-SS"),
            nazov,
            "Fulltext strednej školy"
        )
        self._safe_click(
            self.page.locator("#fulltext-input-SS-button"),
            "Hľadať strednú školu"
        )

    def _click_info(self, eduid: str) -> None:
        self._safe_click(
            self.page.locator(f"#skola-{eduid}").get_by_role("link", name="Viac informácií o škole"),
            f"Viac informácií o škole {eduid}"
        )

    def _zatvor_chat_ak_je_viditelny(self) -> None:
        chat_button = self.page.get_by_role("button", name="Zatvoriť chat")
        if chat_button.is_visible():
            self._safe_click(
                chat_button,
                "Zatvoriť chat"
            )

    def _click_typ_skoly(self, typ: str) -> None:
        self.page.wait_for_timeout(1000)

        item = self.page.locator(f'li:has-text("{typ}")')
        self._safe_click(
            item,
            f"Typ školy - {typ}"
        )

        self._zatvor_chat_ak_je_viditelny()

        classes = item.get_attribute("class") or ""
        if "navigation-item-active" not in classes:
            self._safe_click(
                item,
                f"Typ školy - {typ} opakovanie"
            )

    def vyhladaj_skolu(self, nazov: str, eduid: str, typ: str):
        self._click_on_najst_skolu()
        self._click_typ_skoly(typ)

        if typ == self.TYP_SS:
            self._hladat_SS(nazov)
        else:
            self._hladat_podla_nazvu(nazov)

        self._click_info(eduid)
        self.page.wait_for_load_state("networkidle")

    def click_on_profil_skoly(self) -> None:
        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť profil školy"),
            "Zobraziť profil školy"
        )

    def rozklikni_SS(self):
        self._safe_click(
            self.page.get_by_text("add").first,
            "Rozkliknúť sekciu 1"
        )
        self._safe_click(
            self.page.get_by_text("add").first,
            "Rozkliknúť sekciu 2"
        )
        self._safe_click(
            self.page.get_by_text("add").first,
            "Rozkliknúť sekciu 3"
        )
        self._safe_click(
            self.page.get_by_text("add"),
            "Rozkliknúť sekciu 4"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Zobraziť viac").first,
            "Zobraziť viac"
        )