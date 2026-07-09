from playwright.sync_api import Page
from pages.base_page import BasePage


class PrihlaskaMS(BasePage):
    KRAJINA = "Slovenska re"
    KRAJINA_LABEL = "Slovenská republika"
    OBEC = "bobo"
    OBEC_LABEL = "Bobot (Trenčín)"
    ULICA = "debra"
    ULICA_LABEL = "Debraďská"
    SUPISNE_CISLO = "999"
    ORIENTACNE_CISLO = "21"
    PSC = "54231"

    DATUM_DEN = "7"
    DATUM_MESIAC = "9"
    DATUM_ROK = "2026"
    POZNAMKA = "ŠVVP"

    ZZ_MENO = "Fero"
    ZZ_PRIEZVISKO = "Bartoš"
    ZZ_RC = "860224/7005"
    ZZ_EMAIL = "mail@tst.net"
    ZZ_TELEFON = "+421954856321"

    SUBOR_PRILOHA = "./data/Dokument.pdf"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej"),
            nazov_kroku
        )

    def click_on_vytvorit_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_text("Vytvoriť prihlášku").first,
            "Vytvoriť prihlášku"
        )
        self.page.wait_for_load_state("networkidle")
        self._safe_check(
            self.page.get_by_role("radio", name="Materská škola Prihlášku môž"),
            "Typ prihlášky - Materská škola"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať", exact=True),
            "Pridať"
        )
        self.page.wait_for_load_state("networkidle")

    def step_1_pridat_dieta(self, meno: str, priezvisko: str, rc: str):
        self._safe_check(
            self.page.get_by_role("radio", name="Iné dieťa Pridajte dieťa"),
            "Iné dieťa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať dieťa"),
            "Pridať dieťa"
        )
        self.page.wait_for_load_state("networkidle")

        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Dieťa má rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            rc,
            "Rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Krstné meno *"),
            meno,
            "Krstné meno"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            priezvisko,
            "Priezvisko"
        )
        self._safe_click(
            self.page.locator("#step-1").get_by_role("button", name="Ďalej"),
            "Ďalej - krok 1"
        )

        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )
        self._safe_fill(
            self.page.locator("#adresaTPKrajina").get_by_role("textbox"),
            self.KRAJINA,
            "Krajina"
        )
        self._safe_click(
            self.page.locator("#adresaTPKrajina").get_by_text(self.KRAJINA_LABEL, exact=True),
            "Slovenská republika"
        )

        self._safe_fill(
            self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input"),
            self.OBEC,
            "Obec"
        )
        self._safe_click(
            self.page.get_by_text(self.OBEC_LABEL),
            "Bobot (Trenčín)"
        )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Krajina *"),
            self.ULICA,
            "Ulica"
        )
        self._safe_click(
            self.page.get_by_text(self.ULICA_LABEL),
            "Debraďská"
        )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Súpisné číslo"),
            self.SUPISNE_CISLO,
            "Súpisné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Orientačné číslo *"),
            self.ORIENTACNE_CISLO,
            "Orientačné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="PSČ *"),
            self.PSC,
            "PSČ"
        )

        self._safe_click(
            self.page.locator("#step-2").get_by_role("button", name="Pridať dieťa"),
            "Pridať dieťa - potvrdenie"
        )
        self._click_dalej("Ďalej po pridaní dieťaťa")
        self._click_dalej("Ďalej na ďalší krok")

    def step_2_SVVP(self):
        self._safe_check(
            self.page.get_by_role("radio", name="Celodennú výchovu a vzdelá"),
            "Celodennú výchovu a vzdelávanie"
        )
        self._safe_check(
            self.page.locator("#DPDSVVPRadio_option_1"),
            "ŠVVP - Nie"
        )
        self._safe_check(
            self.page.locator("#DPDDietaSNadanimRadio_option_1"),
            "Dieťa s nadaním - Nie"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Deň"),
            self.DATUM_DEN,
            "Deň"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Mesiac"),
            self.DATUM_MESIAC,
            "Mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rok"),
            self.DATUM_ROK,
            "Rok"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Poznámka:"),
            self.POZNAMKA,
            "Poznámka"
        )
        self._click_dalej("Ďalej - krok SVVP")

    def step_3_vyber_skoly(self, nazov: str):
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
        self._safe_click(
            self.page.get_by_role("button", name="Materská škola pre AT Pridať do prihlášky"),
            "Pridať školu do prihlášky"
        )
        self._click_dalej("Ďalej - výber školy 1")
        self._click_dalej("Ďalej - výber školy 2")
        self._click_dalej("Ďalej - výber školy 3")
        self._safe_click(
            self.page.get_by_role("button", name="Mám skontrolované"),
            "Mám skontrolované"
        )

    def step_4_ZZ(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Meno *"),
            self.ZZ_MENO,
            "Meno zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            self.ZZ_PRIEZVISKO,
            "Priezvisko zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            self.ZZ_RC,
            "Rodné číslo zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="E-mail *"),
            self.ZZ_EMAIL,
            "E-mail zákonného zástupcu"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca2Telefon"),
            self.ZZ_TELEFON,
            "Telefón zákonného zástupcu"
        )
        self._click_dalej("Ďalej - krok ZZ 1")
        self._click_dalej("Ďalej - krok ZZ 2")

    def step_5_prilohy(self):
        self._safe_click(
            self.page.get_by_text("Potvrdenie o zdravotnej spôsobilosti (materská škola) Nenahrané Nenahrané"),
            "Potvrdenie o zdravotnej spôsobilosti"
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._click_dalej("Ďalej - prílohy")

    def odoslat_prihlasku_MS(self):
        self._safe_click(
            self.page.locator("#cestnePrehlasenie > .checkmark"),
            "Čestné prehlásenie"
        )
        self._safe_click(
            self.page.locator("#suhlasOsobneUdaje > .checkmark"),
            "Súhlas so spracovaním osobných údajov"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať prihlášku"),
            "Odoslať prihlášku"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať prihlášku").nth(1),
            "Potvrdiť odoslanie prihlášky"
        )

    def vyhladaj_prihlasku(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")
        self._safe_fill(
            self.page.locator("#fulltext-input"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie prihlášky"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self._safe_click(
            self.page.locator("button").filter(has_text="Zobraziť").first,
            "Zobraziť prihlášku"
        )
        self.page.wait_for_load_state("networkidle")