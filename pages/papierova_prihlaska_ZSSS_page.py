from playwright.sync_api import Page
from pages.base_page import BasePage


class PapierovaPrihlaskaZSSS(BasePage):
    KOLO = "2"

    KRAJINA = "slovenska rep"
    KRAJINA_LABEL = "Slovenská republika"
    OBEC = "deb"
    OBEC_LABEL = "Debraď (Košice - okolie)"
    ULICA = "suco"
    ULICA_LABEL = "Súčovská"
    SUPISNE_CISLO = "3"
    ORIENTACNE_CISLO = "9"
    PSC = "65874"

    ZZ1_MENO = "Rudolf"
    ZZ1_PRIEZVISKO = "Brezinoha"
    ZZ1_RC = "760225/6013"
    ZZ1_EMAIL = "katalontest987@gmail.com"
    ZZ1_TELEFON = "+421987654321"

    ZZ2_MENO = "Tereza"
    ZZ2_PRIEZVISKO = "Brezinohová"
    ZZ2_RC = "765413/0341"
    ZZ2_EMAIL = "katalontest789@gmail.com"
    ZZ2_TELEFON = "+421357951486"

    TRIEDA = "9.A"
    ROCNIK = "9"
    ROK_SKOLSKEJ_DOCHADZKY = "9"

    SUTAZ_NAZOV = "Ferova dvanástka"
    SUTAZ_DRUH = "9"
    SUTAZ_UROVEN = "4"
    SUTAZ_SKOLSKY_ROK = "2021/2022"

    SUBOR_PRILOHA = "./data/Dokument.pdf"
    POZNAMKA = "ŠVVP"
    POZNAMKA_SKOLY = "(-_-)"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej"),
            nazov_kroku
        )

    def _odstran_predmety(self, pocet: int, nazov_prvku: str):
        for _ in range(pocet):
            self._safe_click(
                self.page.get_by_role("button", name="Odstrániť").nth(1),
                nazov_prvku
            )

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.locator("span:has-text('Prihlášky našich žiakov')"),
            "Prihlášky našich žiakov"
        )
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Kolo"),
            self.KOLO,
            "Kolo"
        )
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku"),
            "Vytvoriť prihlášku"
        )

    def step_1_osobne_udaje(self, meno: str, priezvisko: str, rc: str):
        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Dieťa má rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            rc,
            "Rodné číslo"
        )
        self._click_dalej("Ďalej - rodné číslo")

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
            self.page.get_by_role("textbox", name="Rodné priezvisko"),
            priezvisko,
            "Rodné priezvisko"
        )
        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )

        self._safe_fill(
            self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input"),
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
            "Debraď (Košice - okolie)"
        )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Krajina *"),
            self.ULICA,
            "Ulica"
        )
        self._safe_click(
            self.page.get_by_text(self.ULICA_LABEL),
            "Súčovská"
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

        self._click_dalej("Ďalej - osobné údaje")
        self._click_dalej("Ďalej - pokračovanie po osobných údajoch")

        self._safe_click(
            self.page.get_by_role("button", name="Pokračovať"),
            "Pokračovať"
        )

    def step_2_SVVP(self):
        self._safe_check(
            self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1"),
            "Zmenená pracovná schopnosť - Nie"
        )
        self._safe_check(
            self.page.locator("#specialneVVP_option_1"),
            "Špeciálne výchovno-vzdelávacie potreby - Nie"
        )
        self._safe_check(
            self.page.locator("#mentalnePostihnutie_option_1"),
            "Mentálne postihnutie - Nie"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Poznámka:"),
            self.POZNAMKA,
            "Poznámka"
        )
        self._click_dalej("Ďalej - SVVP")

    def step_3_vyber_skoly(self):
        self._safe_click(
            self.page.get_by_role("link", name="Pridať odbor"),
            "Pridať odbor"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Hľadať podľa názvu školy"),
            "stredná škola pre AT",
            "Hľadať podľa názvu školy"
        )
        self._safe_click(
            self.page.locator("#hladat-podla-nazvu-skoly-button"),
            "Hľadať školu"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať do prihlášky").first,
            "Pridať do prihlášky"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať odbory a odísť"),
            "Pridať odbory a odísť"
        )
        self._click_dalej("Ďalej - výber školy 1")
        self._click_dalej("Ďalej - výber školy 2")

    def step_4_ZZ(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Meno *"),
            self.ZZ1_MENO,
            "Meno zákonného zástupcu 1"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            self.ZZ1_PRIEZVISKO,
            "Priezvisko zákonného zástupcu 1"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            self.ZZ1_RC,
            "Rodné číslo zákonného zástupcu 1"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="E-mail"),
            self.ZZ1_EMAIL,
            "E-mail zákonného zástupcu 1"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Telefónne číslo *"),
            self.ZZ1_TELEFON,
            "Telefónne číslo zákonného zástupcu 1"
        )

        self.page.wait_for_timeout(500)

        radio = self.page.locator("#zastupca2Radio_option_0")
        self._safe_click(radio, "Pridať druhého zákonného zástupcu - prvý klik")
        self._safe_click(radio, "Pridať druhého zákonného zástupcu - druhý klik")

        self._safe_fill(
            self.page.locator("#input-zastupca2Meno"),
            self.ZZ2_MENO,
            "Meno zákonného zástupcu 2"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca2Priezvisko"),
            self.ZZ2_PRIEZVISKO,
            "Priezvisko zákonného zástupcu 2"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca2RodneCislo"),
            self.ZZ2_RC,
            "Rodné číslo zákonného zástupcu 2"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca2Email"),
            self.ZZ2_EMAIL,
            "E-mail zákonného zástupcu 2"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca2Telefon"),
            self.ZZ2_TELEFON,
            "Telefónne číslo zákonného zástupcu 2"
        )

        self._safe_check(
            self.page.get_by_role("radio", name="áno"),
            "Komunikácia s druhým zákonným zástupcom - áno"
        )
        self._safe_click(
            self.page.locator("#komunikaciaLenSZZ1 > .checkmark"),
            "Komunikácia len s druhým zákonným zástupcom"
        )
        self._click_dalej("Ďalej - zákonní zástupcovia")

    def step_5_navsteva_ZS(self):
        self._safe_select(
            self.page.locator("#select-rocnikSKSelect"),
            self.ROCNIK,
            "Ročník"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Trieda *"),
            self.TRIEDA,
            "Trieda"
        )
        self._safe_select(
            self.page.locator("#select-rokSkolskejDochadzkySKSelect"),
            self.ROK_SKOLSKEJ_DOCHADZKY,
            "Rok školskej dochádzky"
        )
        self._safe_click(
            self.page.get_by_role("textbox", name="Názov základnej školy *", exact=True),
            "Názov základnej školy"
        )
        self._safe_click(
            self.page.locator("#vyucovaciJazykVZakladnejSkoleSKAutocomplete").get_by_text("slovenský", exact=True),
            "slovenský"
        )
        self._click_dalej("Ďalej - návšteva ZŠ")

    def step_6_znamky(self):
        self._safe_select(
            self.page.locator("#select-hodnotenie-1-1"),
            "29",
            "Hodnotenie 6. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet zo 6. ročníka")

        self._safe_click(
            self.page.get_by_text("7. ročník"),
            "7. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-2-1"),
            "30",
            "Hodnotenie 7. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet zo 7. ročníka")

        self._safe_click(
            self.page.get_by_text("8. ročník"),
            "8. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-3-1"),
            "31",
            "Hodnotenie 8. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet z 8. ročníka")

        self._safe_click(
            self.page.get_by_text("9. ročník"),
            "9. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-4-1"),
            "29",
            "Hodnotenie 9. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet z 9. ročníka")

        self._click_dalej("Ďalej - známky")

    def step_7_sutaze(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pridať súťaž"),
            "Pridať súťaž"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Názov súťaže *"),
            self.SUTAZ_NAZOV,
            "Názov súťaže"
        )
        self._safe_select(
            self.page.get_by_label("Druh súťaže"),
            self.SUTAZ_DRUH,
            "Druh súťaže"
        )
        self._safe_select(
            self.page.get_by_label("Úroveň súťaže"),
            self.SUTAZ_UROVEN,
            "Úroveň súťaže"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="Bez umiestnenia"),
            "Bez umiestnenia"
        )
        self._safe_select(
            self.page.get_by_label("Školský rok"),
            self.SUTAZ_SKOLSKY_ROK,
            "Školský rok"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať", exact=True),
            "Pridať súťaž"
        )
        self._click_dalej("Ďalej - súťaže")

    def step_8_prilohy(self):
        self._safe_click(
            self.page.locator("span").filter(has_text="Písomné vyhlásenie k podaniam"),
            "Písomné vyhlásenie k podaniam"
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor pre písomné vyhlásenie"
            )
        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._safe_click(
            self.page.get_by_text("Olympiáda / súťaž: Ferova dvanástka Nenahrané Nenahrané Nahrané"),
            "Príloha súťaže Ferova dvanástka"
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.locator("#prilohyUploadZone2").get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor pre prílohu súťaže"
            )
        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._click_dalej("Ďalej - prílohy")

    def step_9_ostatne_udaje(self, den: str, mesiac: str, rok: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Deň"),
            den,
            "Deň"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Mesiac"),
            mesiac,
            "Mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rok"),
            rok,
            "Rok"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Poznámka školy:"),
            self.POZNAMKA_SKOLY,
            "Poznámka školy"
        )
        self._click_dalej("Ďalej - ostatné údaje")

    def click_on_odoslat_prihlasku(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pridať prihlášku"),
            "Pridať prihlášku"
        )
        self.page.wait_for_load_state("load", timeout=15000)

    def najdi_prihlasku(self, meno: str, priezvisko: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie v prihláškach"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )

    def click_on_zobrazit_prihlasku(self):
        self._safe_click(
            self.page.locator("div.riaditel-prihlasky-cell.akcia-cell").locator("button").nth(0),
            "Zobraziť prihlášku"
        )

    def click_on_skontrolovana(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("button", name="Označiť ako skontrolovaná"),
            "Označiť ako skontrolovaná"
        )

    def click_on_odoslat_na_SS(self):
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať na stredné školy"),
            "Odoslať na stredné školy"
        )