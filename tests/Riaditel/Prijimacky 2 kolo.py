import os
import re
import pytest
import utils.data_helper as Data

from utils.mail_helper import Mail
from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.prijimacky_page import Prijimacky
from pages.prihlaska_SS_page import PrihlaskaSS
from utils.pdf_helper import compare_pdf_visual, compare_pdf_text


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _assert_equal(actual: str, expected: str, message: str) -> None:
    assert actual == expected, (
        f"{message}\n\n=== EXPECTED ===\n{expected}\n\n=== ACTUAL ===\n{actual}"
    )


@pytest.mark.regres2kolo
def test_prihlaska_na_SS_2_kolo_prijimacky(page: Page) -> None:
    data = Data.generate_unique_person(min_age=15, max_age=17)
    login = LoginPage(page)
    prihlaska = PrihlaskaSS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku()
    prihlaska.pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_1_vyber_ziaka()
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_ziak_navsteva_skoly()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()
    prihlaska.click_on_odoslat_prihlasku()

    _expect_text(
        page.locator("body"),
        "Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške.",
        "Pred potvrdením odoslania sa nezobrazilo upozornenie o odosielaní prihlášky na stredné školy."
    )
    _expect_text(
        page.locator("body"),
        "Po odoslaní prihlášky už nebude možné upravovať údaje ani prílohy",
        "V potvrdzovacom dialógu chýba upozornenie o nemožnosti ďalšej úpravy údajov."
    )
    _expect_text(
        page.locator("body"),
        "Odoslaním prihlášky sa formálne začne proces jej posúdenia",
        "V potvrdzovacom dialógu chýba informácia o začatí posudzovania prihlášky."
    )

    prihlaska.click_on_potvrdit_odoslanie()

    _expect_url(
        page,
        r".*/Prihlaska-odoslana.*",
        "Po potvrdení odoslania sa neotvorila stránka Prihláška odoslaná."
    )
    _expect_text(
        page.locator("h1"),
        "Prihláška bola úspešne odoslaná!",
        "Po odoslaní prihlášky sa nezobrazil úspešný nadpis."
    )


@pytest.mark.regres2kolo
def test_prijimacky_odoslanie_sprav(page: Page) -> None:
    login = LoginPage(page)
    prijimacky = Prijimacky(page)
    mail = Mail()
    helper = Helper()

    login.login_as_riaditel(username_riad, password_riad, "910021624")

    prijimacky.zmen_kolo_a_odbor()
    prijimacky.zorad_prihlasky()
    prijimacky.zobraz_prihlasku_detail()

    pristupovy_kod, meno, priezvisko, datum_narodenia = prijimacky.get_udaje_dietata()

    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()
    prijimacky.click_on_uprava_prihlasky()

    _expect_text(
        page.locator("#prij_edit_meno"),
        f"{priezvisko} {meno}",
        "V úprave prihlášky sa nezobrazuje správne meno žiaka."
    )
    _expect_text(
        page.locator("#prij_edit_detaily"),
        "O4 - zlievač • slovenský • 2285H00",
        "V úprave prihlášky sa nezobrazujú správne detaily odboru."
    )

    prijimacky.nastavenie_terminu_prijimaciek()
    prijimacky.click_on_akcia_odoslat_pozvanky()

    _expect_text(
        page.locator("body"),
        "Vygenerovať pozvánky",
        "Nezobrazil sa dialóg pre generovanie pozvánok."
    )

    prijimacky.odoslat_pozvanky()

    pozvanka = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    pozvanka = helper.cleanup_email_text(pozvanka)

    expected_pozvanka = (
        f"Vážený/á pán/pani Mária Bartošová týmto pozývame žiaka {meno} {priezvisko} {datum_narodenia} "
        f"na prijímaciu skúšku 1. termín (2.kolo) do odboru vzdelávania 2285H00-zlievač , v škole "
        f"Stredná škola pre AT, ktorá sa uskutoční dňa 12.10.2026 o 11:30 hod. Miesto: Stredná škola pre AT, 3.E "
        f"Váš prístupový kód: {pristupovy_kod}. Odporúčame si ho bezpečne uložiť. Predmety prijímacej skúšky "
        f"Matematika, Slovenský jazyk a literatúra. Dostavte sa na čas a prineste si kružítko. "
        f"S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
        f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_equal(
        pozvanka,
        expected_pozvanka,
        "Obsah e-mailu s pozvánkou na prijímacie skúšky nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#prijimacky-generovanie-spustene"),
        "Generovanie 1 pozvánok bolo spustené.",
        "Po odoslaní pozvánok sa nezobrazila informácia o spustení generovania."
    )
    _expect_text(
        page.locator("#prijimacky-generovanie-spustene"),
        "Tento proces môže v závislosti od počtu vybraných pozvánok trvať niekoľko minút až hodín.",
        "Po odoslaní pozvánok chýba informácia o trvaní generovania."
    )

    prijimacky.click_on_spat_na_prijimacky()
    prijimacky.zmen_kolo_a_odbor()
    prijimacky.zorad_prihlasky()

    _expect_visible(
        page.locator("div.riaditel-prijimacky-cell.komunikacia-cell").locator("div").nth(2),
        "V zozname prijímačiek sa nezobrazuje ikona komunikácie po odoslaní pozvánky."
    )

    prijimacky.click_on_akcia_plny_pocet_bodov()

    _expect_text(
        page.locator("body"),
        "Vygenerovať správu o plnom počte bodov",
        "Nezobrazil sa dialóg pre správu o plnom počte bodov."
    )

    prijimacky.odoslat_plny_pocet_bodov()

    plny_pocet = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    plny_pocet = helper.cleanup_email_text(plny_pocet)

    expected_plny_pocet = (
        f"Vážený/á pán/pani Mária Bartošová žiak {meno} {priezvisko} {datum_narodenia} splnil podmienky "
        f"na dosiahnutie plného počtu bodov z prijímacích skúšok do odboru vzdelávania 2285H00-zlievač , "
        f"v škole Stredná škola pre AT, ktoré mu boli udelené v systéme. Výsledky prijímacieho konania si môžete "
        f"pozrieť, keď budú dostupné pod číselným prístupovým kódom, ktorý bol žiakovi pridelený. "
        f"Váš prístupový kód: {pristupovy_kod}. Odporúčame si ho bezpečne uložiť. Prosím, zapíšte si ho. "
        f"S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
        f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_equal(
        plny_pocet,
        expected_plny_pocet,
        "Obsah e-mailu o plnom počte bodov nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#riaditel-home-page"),
        "Správa bola úspešne odoslaná",
        "Po odoslaní správy o plnom počte bodov sa nezobrazila úspešná hláška."
    )

    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.zmen_kolo_a_odbor()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()

    prijimacky.stiahni_pozvanku()
    prijimacky.stiahni_body()


@pytest.mark.regres2kolo
def test_porovnaj_body_pdf_vizualne() -> None:
    compare_pdf_visual(
        actual_pdf="data/downloads/bodyDownloaded.pdf",
        expected_pdf="data/BodyPredloha.pdf",
        masks={
            0: [
                (100, 300, 400, 330),
                (300, 450, 500, 480),
                (250, 250, 450, 290),
            ],
        },
        threshold=0.05,
        max_diff_pixels=5000,
        name_prefix="body_pdf",
        zoom=2.0,
    )


@pytest.mark.regres2kolo
def test_porovnaj_body_pdf_textovo() -> None:
    compare_pdf_text(
        actual_pdf="data/downloads/bodyDownloaded.pdf",
        expected_pdf="data/BodyPredloha.pdf",
        name_prefix="body_text",
        flatten_to_single_line=True,
        ignore_patterns=[
            r"(?<=žiak\s)[^\d]+?(?=\d{2}\.\d{2}\.\d{4})",
            r"Mária Bartošová",
            r"(?<!\d)\d{2}\.\d{2}\.\d{4}(?!\d)",
            r"(?<=Váš prístupový kód:\s)[A-Za-z0-9]+",
        ],
    )


@pytest.mark.regres2kolo
def test_porovnaj_pozvanka_pdf_vizualne() -> None:
    compare_pdf_visual(
        actual_pdf="data/downloads/pozvankaDownloaded.pdf",
        expected_pdf="data/PozvánkaPredloha2kolo.pdf",
        masks={
            0: [
                (320, 300, 610, 340),
                (200, 440, 500, 500),
                (270, 250, 460, 290),
                (400, 400, 450, 450),
            ],
        },
        threshold=0.05,
        max_diff_pixels=5000,
        name_prefix="pozvanka_pdf",
        zoom=2.0,
    )


@pytest.mark.regres2kolo
def test_porovnaj_pozvanka_pdf_textovo() -> None:
    compare_pdf_text(
        actual_pdf="data/downloads/pozvankaDownloaded.pdf",
        expected_pdf="data/PozvánkaPredloha2kolo.pdf",
        name_prefix="pozvanka_text",
        flatten_to_single_line=True,
        ignore_patterns=[
            r"(?<=žiaka\s)[^\d]+?(?=\d{2}\.\d{2}\.\d{4})",
            r"Mária Bartošová",
            r"(?<!\d)\d{2}\.\d{2}\.\d{4}(?!\d)",
            r"(?<=Váš prístupový kód:\s)[A-Za-z0-9]+",
        ],
    )