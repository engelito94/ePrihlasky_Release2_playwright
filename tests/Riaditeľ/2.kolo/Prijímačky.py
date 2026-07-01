import pytest
import os
import re
import utils.data_helper as Data
from utils.mail_helper import Mail
from utils.helpers import Helper
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prijimacky_page import Prijimacky
from pages.prihlaska_SS_page import PrihlaskaSS
from utils.pdf_helper import compare_pdf_visual, export_pdf_page_for_masks


mailuser=os.getenv("GMAIL_USERNAME")
mailpw=os.getenv("GMAIL_APP_PASSWORD")
username=os.getenv("EPRIHLASKY_ZZ_USERNAME")
password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")

#get_by_role("button", name="Stredná škola pre AT Pridať").nth(4)

@pytest.mark.regression
def test_prihlaska_na_SS_2_kolo_prijimacky(page: Page) -> None:
    data = Data.pop_random_person_from_file("./data/detiSS.txt")
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
    expect(page.locator("body")).to_contain_text("Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške. Po odoslaní prihlášky už nebude možné upravovať údaje ani prílohy, pokiaľ vás na opravu nevyzve riaditeľ školy. Pred odoslaním si preto dôkladne skontrolujte všetky údaje a priložené dokumenty. Odoslaním prihlášky sa formálne začne proces jej posúdenia podľa zákona č. 71/1967 Zb. o správnom konaní (správny poriadok).")
    prihlaska.click_on_potvrdit_odoslanie()
    expect(page).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=35000)
    expect(page.locator("h1")).to_contain_text("Prihláška bola úspešne odoslaná!")
    
@pytest.mark.regression
def test_prijimacky_odoslanie_sprav(page: Page) -> None:
    login = LoginPage(page)
    prijimacky = Prijimacky(page)
    mail = Mail()
    helper = Helper()
    login.login_as_riaditel(username_riad,password_riad,"910021624")
    prijimacky.zmen_kolo_a_odbor()
    prijimacky.zorad_prihlasky()
    prijimacky.zobraz_prihlasku_detail()
    pristupovy_kod, meno, priezvisko, datum_narodenia = prijimacky.get_udaje_dietata()
    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()
    prijimacky.click_on_uprava_prihlasky()
    expect(page.locator("#prij_edit_meno")).to_contain_text(priezvisko +" "+ meno)
    expect(page.locator("#prij_edit_detaily")).to_contain_text("O4 - zlievač • slovenský • 2285H00")
    prijimacky.nastavenie_terminu_prijimaciek()
    prijimacky.click_on_akcia_odoslat_pozvanky()
    expect(page.locator("body")).to_contain_text("Vygenerovať pozvánky")
    prijimacky.odoslat_pozvanky()

    pozvanka = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    pozvanka = helper.cleanup_email_text(pozvanka)
    expected = f"Vážený/á pán/pani Mária Bartošová týmto pozývame žiaka {meno} {priezvisko} {datum_narodenia} na prijímaciu skúšku 1. termín (2.kolo) do odboru vzdelávania 2285H00-zlievač , v škole Stredná škola pre AT, ktorá sa uskutoční dňa 12.10.2026 o 11:30 hod. Miesto: Stredná škola pre AT, 3.E Váš prístupový kód: {pristupovy_kod}. Odporúčame si ho bezpečne uložiť. Predmety prijímacej skúšky Matematika, Slovenský jazyk a literatúra. Dostavte sa na čas a prineste si kružítko. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    assert pozvanka == expected

    expect(page.locator("#prijimacky-generovanie-spustene")).to_contain_text("Generovanie 1 pozvánok bolo spustené.")
    expect(page.locator("#prijimacky-generovanie-spustene")).to_contain_text("Tento proces môže v závislosti od počtu vybraných pozvánok trvať niekoľko minút až hodín.")
    prijimacky.click_on_spat_na_prijimacky()
    prijimacky.zmen_kolo_a_odbor()
    prijimacky.zorad_prihlasky()
    expect(page.locator("div.riaditel-prijimacky-cell.komunikacia-cell").locator("div").nth(2)).to_be_visible()
    prijimacky.click_on_akcia_plny_pocet_bodov()
    expect(page.locator("body")).to_contain_text("Vygenerovať správu o plnom počte bodov")
    prijimacky.odoslat_plny_pocet_bodov()

    plny_pocet = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    plny_pocet = helper.cleanup_email_text(plny_pocet)
    expected = f"Vážený/á pán/pani Mária Bartošová žiak {meno} {priezvisko} {datum_narodenia} splnil podmienky na dosiahnutie plného počtu bodov z prijímacích skúšok do odboru vzdelávania 2285H00-zlievač , v škole Stredná škola pre AT, ktoré mu boli udelené v systéme. Výsledky prijímacieho konania si môžete pozrieť, keď budú dostupné pod číselným prístupovým kódom, ktorý bol žiakovi pridelený. Váš prístupový kód: {pristupovy_kod}. Odporúčame si ho bezpečne uložiť. Prosím, zapíšte si ho. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    assert plny_pocet == expected

    expect(page.locator("#riaditel-home-page")).to_contain_text("Správa bola úspešne odoslaná")

    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.zmen_kolo_a_odbor()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()

    prijimacky.stiahni_pozvanku()
    prijimacky.stiahni_body()


@pytest.mark.regression
def test_porovnaj_body_pdf():
    compare_pdf_visual(
        actual_pdf="data/downloads/bodyDownloaded.pdf",
        expected_pdf="data/BodyPredloha.pdf",
        masks={
            0: [
                (100, 300, 400, 330),   # meno a priezvisko
                (300, 450, 500, 480),   # kod
                (250, 250, 450, 290),   # meno rodič
            ],
        },
        threshold=0.05,
        max_diff_pixels=5000,
        name_prefix="body_pdf",
        zoom=2.0,
    )

    
@pytest.mark.regression
def test_porovnaj_pozvanka_pdf():
    compare_pdf_visual(
        actual_pdf="data/downloads/pozvankaDownloaded.pdf",
        expected_pdf="data/PozvánkaPredloha2kolo.pdf",
        masks={
            0: [
                (320, 300, 610, 340),   # meno a priezvisko
                (200, 440, 500, 500),   # kod
                (270, 250, 460, 290),   # meno rodič
                (400, 400, 450, 450),   # trieda
            ],
        },
        threshold=0.05,
        max_diff_pixels=5000,
        name_prefix="pozvanka_pdf",
        zoom=2.0,
    )