import os
import re
import pytest
import utils.data_helper as Data

from utils.helpers import Helper
from utils.mail_helper import Mail
from playwright.sync_api import Page, expect

from pages.logout_page import LogoutPage
from pages.login_page import LoginPage
from pages.prihlaska_MS_page import PrihlaskaMS
from pages.papierova_prihlaska_MS_page import PapierovaPrihlaskaMS
from pages.konflikt_MS_page import KonfliktMS


username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")
mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=4, max_age=5)


def _expect_text(locator, text: str, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _normalize_email_text(raw_email: str, helper: Helper) -> str:
    return helper.cleanup_email_text(raw_email)


def _assert_email_in_options(actual: str, options: list[str], message: str) -> None:
    assert actual in options, (
        f"{message}\n\n"
        f"=== ACTUAL ===\n{actual}\n\n"
        f"=== EXPECTED OPTIONS ===\n" + "\n---\n".join(options)
    )


def _create_electronic_ms_application(page: Page, data) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaMS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku()
    prihlaska.step_1_pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("materská škola pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_prilohy()
    prihlaska.odoslat_prihlasku_MS()

    _expect_url(
        page,
        r".*/Prihlaska-odoslana.*",
        "Po odoslaní elektronickej prihlášky sa neotvorila stránka Prihláška odoslaná."
    )
    _expect_text(
        page.locator("h1"),
        "Prihláška bola úspešne odoslaná!",
        "Po odoslaní elektronickej prihlášky sa nezobrazil úspešný nadpis."
    )

    logout.logout()


def _create_paper_ms_application(page: Page, data, helper: Helper) -> None:
    login = LoginPage(page)
    prihlaska_riad = PapierovaPrihlaskaMS(page)
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username_riad, password_riad, "910021626")
    _expect_url(
        page,
        r".*/Riaditel.*",
        "Po prihlásení riaditeľa sa neotvorila stránka riaditeľa."
    )

    prihlaska_riad.click_on_pridaj_prihlasku()
    prihlaska_riad.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska_riad.step_2_SVVP()
    prihlaska_riad.step_3_vyber_skoly()
    prihlaska_riad.step_4_ZZ()
    prihlaska_riad.step_5_prilohy()
    prihlaska_riad.step_6_ostatne_udaje(den, mesiac, rok)
    prihlaska_riad.click_on_odoslat_prihlasku()

    _expect_url(
        page,
        r".*/Riaditel.*",
        "Po odoslaní papierovej prihlášky sa nevrátila stránka riaditeľa.",
        timeout=60000
    )
    _expect_text(
        page.locator("#riaditel-home-page"),
        "Prihlášku pre dieťa ste úspešne pridali.",
        "Po odoslaní papierovej prihlášky sa nezobrazila úspešná hláška."
    )


def _build_conflict_notice_options(data, helper: Helper) -> list[str]:
    return [
        (
            f"Vážený/á pán/pani Peter Fodrok, v systéme bolo zistené, že pre žiaka "
            f"{data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)} "
            f"boli podané viaceré prihlášky. Riaditeľ školy Materská škola pre AT Vás týmto vyzýva, "
            f"aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. "
            f"Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu "
            f"nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR "
            f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe "
            f"Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Mária Bartošová, v systéme bolo zistené, že pre žiaka "
            f"{data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)} "
            f"boli podané viaceré prihlášky. Riaditeľ školy Materská škola pre AT Vás týmto vyzýva, "
            f"aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. "
            f"Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu "
            f"nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR "
            f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe "
            f"Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
    ]


def _build_resolution_options(
    typ_prihlasky: str,
    identifikator: str,
    identifikator1: str,
    data,
    helper: Helper,
) -> list[str]:
    if typ_prihlasky == "Elektronicky":
        return [
            (
                f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte "
                f"s prihláškou/prihláškami {identifikator}, {identifikator1}. Konflikt bol vyriešený . "
                f"V systéme bude ďalej evidovaná len prihláška {identifikator}. S pozdravom "
                f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
                f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, "
                f"vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
            ),
            (
                f"Vážený/á pán/pani Peter Fodrok, riaditeľ školy Materská škola pre AT vyriešil konflikt "
                f"viacerých prihlášok podaných pre žiaka {data.meno} {data.priezvisko} nar. "
                f"{helper.rc_to_datum_narodenia(data.rodne_cislo)}. Ako aktívna bola označená prihláška "
                f"s identifikátorom {identifikator}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky "
                f"boli označené ako “Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete "
                f"overiť po prihlásení do portálu Elektronické prihlášky: Link na prihlásenie S pozdravom "
                f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
                f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja "
                f"a mládeže Slovenskej republiky. Neodpovedajte naň."
            ),
        ]

    return [
        (
            f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator1} bola v konflikte "
            f"s prihláškou/prihláškami {identifikator1}, {identifikator}. Konflikt bol vyriešený . "
            f"V systéme bude ďalej evidovaná len prihláška {identifikator1}. S pozdravom "
            f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
            f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, "
            f"vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Peter Fodrok, riaditeľ školy Materská škola pre AT vyriešil konflikt "
            f"viacerých prihlášok podaných pre dieťa {data.meno} {data.priezvisko} nar. "
            f"{helper.rc_to_datum_narodenia(data.rodne_cislo)}. Ako aktívna bola označená prihláška "
            f"s identifikátorom {identifikator1}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky "
            f"boli označené ako “Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete "
            f"overiť po prihlásení do portálu Elektronické prihlášky: Link na prihlásenie S pozdravom "
            f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
            f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja "
            f"a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Peter Fodrok, riaditeľ školy Materská škola pre AT vyriešil konflikt "
            f"viacerých prihlášok podaných pre dieťa {data.meno} {data.priezvisko} nar. "
            f"{helper.rc_to_datum_narodenia(data.rodne_cislo)}. Ako aktívna bola označená prihláška "
            f"s identifikátorom {identifikator}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky "
            f"boli označené ako “Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete "
            f"overiť po prihlásení do portálu Elektronické prihlášky: Link na prihlásenie S pozdravom "
            f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
            f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja "
            f"a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte "
            f"s prihláškou/prihláškami {identifikator}, {identifikator1}. Konflikt bol vyriešený . "
            f"V systéme bude ďalej evidovaná len prihláška {identifikator}. S pozdravom "
            f"Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
            f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, "
            f"vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
    ]


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_vytvorenie_konfliktu_na_MS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()

    _create_electronic_ms_application(page, data)
    _create_paper_ms_application(page, data, helper)


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_vyriesenie_konfliktu_na_MS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    prihlaska = PrihlaskaMS(page)
    konflikt = KonfliktMS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)

    conflict_panel = page.locator("#info-panel-red-prihlaska-v-konflikte-riad-zs")
    _expect_text(conflict_panel, "Táto prihláška je v stave - V konflikte.", "Chýba informácia, že prihláška je v konflikte.")
    _expect_text(conflict_panel, "Vyzvite zákonného zástupcu na výber jednej verzie.", "Chýba výzva na kontaktovanie zákonného zástupcu.")
    _expect_text(conflict_panel, "Následne vyriešte konflikt označením jednej prihlášky ako aktívnej.", "Chýba popis ďalšieho kroku riešenia konfliktu.")

    typ_prihlasky = page.locator("#detail-prihlasky-riad-MS-ZS-content").text_content()
    identifikator = page.locator("div.prihlaska-v-konflikte-item").locator("div").nth(0).text_content()[1:]
    identifikator1 = page.locator("div.prihlaska-v-konflikte-item").locator("div").nth(2).text_content()[1:]

    konflikt.click_on_vyzva_na_vyriesenie_konfliktu()

    _expect_text(
        page.locator("#vyzva-riesenie-konfliktu-title"),
        "Výzva na riešenie konfliktu",
        "Nezobrazil sa dialóg Výzva na riešenie konfliktu."
    )
    _expect_text(
        page.locator("body"),
        "Pre dieťa existuje viac ako jedna prihláška.",
        "V dialógu výzvy chýba informácia o viacerých prihláškach."
    )
    _expect_text(page.locator("body"), "Peter Fodrok", "V dialógu výzvy chýba meno Peter Fodrok.")
    _expect_text(page.locator("body"), "Mária Bartošová", "V dialógu výzvy chýba meno Mária Bartošová.")

    konflikt.odoslat_vyzvu_na_vyriesenie_konfliktu()

    vyzva_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyzva_konflikt = _normalize_email_text(vyzva_konflikt, helper)

    _assert_email_in_options(
        vyzva_konflikt,
        _build_conflict_notice_options(data, helper),
        "Obsah e-mailu s výzvou na vyriešenie konfliktu nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        "Riaditeľ školy Materská škola pre AT zaslal výzvu na riešenie konfliktu prihlášok.",
        "Po odoslaní výzvy sa nezobrazila informácia o zaslanej výzve."
    )

    konflikt.click_on_vyriesenie_konfliktu()

    _expect_text(
        page.locator("#vyriesit-konflikt-title"),
        "Vyriešiť konflikt",
        "Nezobrazil sa dialóg Vyriešiť konflikt."
    )
    _expect_text(
        page.locator("body"),
        "Po označení prihlášky ako aktívnej sa automaticky zneaktívnia všetky duplicitné prihlášky",
        "V dialógu riešenia konfliktu chýba vysvetlenie dôsledku označenia aktívnej prihlášky."
    )

    konflikt.odoslat_vyriesenie_konfliktu("Vyriešenie konfliktu.")

    vyriesenie_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyriesenie_konflikt = _normalize_email_text(vyriesenie_konflikt, helper)

    _assert_email_in_options(
        vyriesenie_konflikt,
        _build_resolution_options(typ_prihlasky, identifikator, identifikator1, data, helper),
        "Obsah e-mailu o vyriešení konfliktu nezodpovedá očakávaniu."
    )

    _expect_text(
        page.get_by_role("strong"),
        "Duplicita prihlášok úspešne vyriešená",
        "Chýba zvýraznená hláška o úspešnom vyriešení duplicity."
    )
    _expect_text(
        page.locator("#info-panel-green-konflikt-vyrieseny"),
        "Duplicita prihlášok úspešne vyriešená",
        "Chýba zelený panel o vyriešení duplicity."
    )
    _expect_text(
        page.locator("#info-panel-green-konflikt-vyrieseny"),
        "Všetky duplicitné prihlášky boli zneaktívnené.",
        "V zelenom paneli chýba informácia o zneaktívnení duplicitných prihlášok."
    )
    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        f"Pre dieťa {data.meno} {data.priezvisko} bol vyriešený konflikt.",
        "V detaile duplicity chýba informácia o vyriešenom konflikte."
    )

    if typ_prihlasky == "Elektronicky":
        _expect_text(
            page.locator("#info-panel-blue-prihlaska-aktivna"),
            "Prihláška bola označená ako aktívna riaditeľom školy 910021626 Materská škola pre AT",
            "Chýba modrý panel o označení aktívnej prihlášky."
        )
        _expect_text(
            page.locator("#detail-prihlasky-riad-MS-ZS-content"),
            "Podaná",
            "Po vyriešení konfliktu nemá aktívna prihláška stav 'Podaná'."
        )