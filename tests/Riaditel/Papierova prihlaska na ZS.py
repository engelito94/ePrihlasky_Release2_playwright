import os
import re
import pytest
import utils.data_helper as Data
from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.papierova_prihlaska_ZS_page import PapierovaPrihlaskaZS


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str):
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str):
    expect(locator, message).to_be_visible()


def _expect_zs_pdp_dietata(page: Page) -> None:
    locator = page.locator("#pdpDietata")

    _expect_text(locator, "Žiadam o prijatie dieťaťa na", "V sekcii požadovaných údajov chýba úvodný text.")
    _expect_text(locator, "Požadovaná výchova Etická", "V sekcii požadovaných údajov chýba požadovaná výchova.")
    _expect_text(locator, "Záujem o stravovanie v školskej jedálni Áno", "Chýba údaj o záujme o stravovanie.")
    _expect_text(locator, "Záujem o školský klub detí Nie", "Chýba údaj o záujme o školský klub.")
    _expect_text(locator, "Zdravotné znevýhodnenie dieťaťa Nie", "Chýba údaj o zdravotnom znevýhodnení.")
    _expect_text(locator, "Dieťa s nadaním Nie", "Chýba údaj o nadaní dieťaťa.")
    _expect_text(locator, "Požadovaný dátum prijatia dieťaťa do materskej školy -", "Chýba požadovaný dátum prijatia.")
    _expect_text(locator, "Popis znevýhodnenia", "Chýba položka Popis znevýhodnenia.")
    _expect_text(locator, "Popis nadania", "Chýba položka Popis nadania.")
    _expect_text(locator, "Poznámka ŠVVP", "Chýba poznámka ŠVVP.")
    _expect_text(locator, "Pokračovanie v plnení povinného predprimárneho vzdelávania -", "Chýba údaj o pokračovaní povinného predprimárneho vzdelávania.")
    _expect_text(locator, "Zmenená pracovná schopnosť -", "Chýba údaj o zmene pracovnej schopnosti.")
    _expect_text(locator, "Špeciálne výchovno-vzdelávacie potreby -", "Chýba údaj o ŠVVP.")
    _expect_text(locator, "Mentálne postihnutie -", "Chýba údaj o mentálnom postihnutí.")
    _expect_text(locator, "Poznámka -", "Chýba finálna poznámka v sekcii požadovaných údajov.")


def _expect_zs_school_section(page: Page) -> None:
    locator = page.locator("#skoly")

    _expect_text(locator, "1 Základná škola č. 1", "V sekcii školy chýba poradie školy.")
    _expect_text(locator, "Názov školy Základná škola pre AT", "V sekcii školy chýba názov školy.")
    _expect_text(locator, "Sídlo základnej školy Jalmová 266/19, 06534 Prešov", "V sekcii školy chýba sídlo školy.")
    _expect_text(locator, "Vzdelávanie dieťaťa žiadam poskytovať v jazyku slovenský", "V sekcii školy chýba vyučovací jazyk.")
    _expect_text(locator, "Záujem o prípravný ročník Nie", "V sekcii školy chýba údaj o prípravnom ročníku.")
    _expect_text(locator, "Záujem o úvodný ročník Nie", "V sekcii školy chýba údaj o úvodnom ročníku.")


def _expect_zs_guardians_section(page: Page) -> None:
    locator = page.locator("#zastupcovia")

    _expect_text(locator, "Osobné údaje zákonného zástupcu č. 1", "Chýba hlavička zákonného zástupcu č. 1.")
    _expect_text(locator, "Meno Patrik", "Chýba meno zákonného zástupcu č. 1.")
    _expect_text(locator, "Priezvisko Kvarga", "Chýba priezvisko zákonného zástupcu č. 1.")
    _expect_text(locator, "Rodné priezvisko -", "Chýba rodné priezvisko zákonného zástupcu č. 1.")
    _expect_text(locator, "Rodné číslo 650204/9367", "Chýba rodné číslo zákonného zástupcu č. 1.")
    _expect_text(locator, "Číslo elektronickej schránky -", "Chýba číslo elektronickej schránky zákonného zástupcu č. 1.")
    _expect_text(locator, "Dátum narodenia 04.02.1965", "Chýba dátum narodenia zákonného zástupcu č. 1.")
    _expect_text(locator, "Korešpondenčná adresa New Dhili, 879/71, Indická republika", "Chýba korešpondenčná adresa zákonného zástupcu č. 1.")
    _expect_text(locator, "E-mail -", "Chýba e-mail zákonného zástupcu č. 1.")
    _expect_text(locator, "Telefónne číslo +421966332557", "Chýba telefón zákonného zástupcu č. 1.")
    _expect_text(locator, "Súhlas s komunikáciou výhradne so zákonným zástupcom č. 1 -", "Chýba údaj o súhlase s komunikáciou.")

    _expect_text(locator, "Osobné údaje zákonného zástupcu č. 2", "Chýba hlavička zákonného zástupcu č. 2.")
    _expect_text(locator, "Meno -", "Chýba údaj o mene zákonného zástupcu č. 2.")
    _expect_text(locator, "Priezvisko -", "Chýba údaj o priezvisku zákonného zástupcu č. 2.")
    _expect_text(locator, "Rodné priezvisko -", "Chýba rodné priezvisko zákonného zástupcu č. 2.")
    _expect_text(locator, "Rodné číslo -", "Chýba rodné číslo zákonného zástupcu č. 2.")
    _expect_text(locator, "Dátum narodenia -", "Chýba dátum narodenia zákonného zástupcu č. 2.")
    _expect_text(locator, "Korešpondenčná adresa -", "Chýba korešpondenčná adresa zákonného zástupcu č. 2.")
    _expect_text(locator, "E-mail -", "Chýba e-mail zákonného zástupcu č. 2.")
    _expect_text(locator, "Telefónne číslo -", "Chýba telefónne číslo zákonného zástupcu č. 2.")
    _expect_text(locator, "Čestne vyhlasujem, že s podaním prihlášky súhlasí aj druhý zákonný zástupca dieťaťa -", "Chýba čestné vyhlásenie o druhom zákonnom zástupcovi.")
    _expect_text(locator, "Dôvod, prečo nebolo dané čestné vyhlásenie o súhlase druhého zákonného zástupcu s podaním prihlášky -", "Chýba dôvod k čestnému vyhláseniu.")
    _expect_text(locator, "Druhý zákonný zástupca nie je známy.", "Chýba informácia, že druhý zákonný zástupca nie je známy.")

    _expect_text(locator, "Názov zariadenia -", "Chýba názov zariadenia.")
    _expect_text(locator, "IČO zariadenia -", "Chýba IČO zariadenia.")
    _expect_text(locator, "Adresa zariadenia -", "Chýba adresa zariadenia.")
    _expect_text(locator, "Číslo elektronickej schránky -", "Chýba elektronická schránka zariadenia.")
    _expect_text(locator, "E-mail -", "Chýba e-mail zariadenia.")
    _expect_text(locator, "Telefónne číslo -", "Chýba telefónne číslo zariadenia.")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_pridanie_papierovej_prihlasky_ZS(page: Page) -> None:
    data = Data.generate_unique_person(min_age=6, max_age=8)
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaZS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username, password, "910021625")
    prihlaska.click_on_pridaj_prihlasku()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_4_ZZ()
    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)

    _expect_zs_pdp_dietata(page)
    _expect_zs_school_section(page)
    _expect_zs_guardians_section(page)

    _expect_text(
        page.locator("#prilohyContainer"),
        "Neboli nahrané žiadne prílohy.",
        "V sekcii príloh chýba informácia, že neboli nahrané žiadne prílohy."
    )

    prihlaska.click_on_odoslat_prihlasku()

    expect(
        page,
        "Po odoslaní papierovej prihlášky ZŠ sa neotvorila stránka riaditeľa."
    ).to_have_url(re.compile(r".*/Riaditel.*"), timeout=60000)

    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)

    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        f"{data.priezvisko} {data.meno}",
        "V zozname prihlášok sa nenašlo meno a priezvisko dieťaťa."
    )
    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        "Papierovo",
        "V zozname prihlášok sa nezobrazuje spôsob podania 'Papierovo'."
    )