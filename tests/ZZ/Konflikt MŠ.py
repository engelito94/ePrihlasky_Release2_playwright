import pytest
import os
import re
import utils.data_helper as Data
from utils.helpers import Helper 
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prihlaska_MS_page import PrihlaskaMS
from pages.papierova_prihlaska_MS_page import PapierovaPrihlaskaMS
from pages.konflikt_MS_page import konfliktMS


username=os.getenv("EPRIHLASKY_ZZ_USERNAME")
password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")
mailuser=os.getenv("GMAIL_USERNAME")
mailpw=os.getenv("GMAIL_APP_PASSWORD")

@pytest.fixture(scope="module")
def test_data():
    data = Data.pop_random_person_from_file("./data/detiMS.txt")

    return {
        "data": data,
    }

@pytest.mark.regression
def test_vytvorenie_konfliktu_na_MŠ(page: Page, test_data) -> None:
    data = test_data["data"]
    helper = Helper()
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
    expect(page).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=35000)
    expect(page.locator("h1")).to_contain_text("Prihláška bola úspešne odoslaná!")
    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    expect(page).to_have_url(re.compile(r".*/Riaditel*"), timeout=35000)
    prihlaskaRiad = PapierovaPrihlaskaMS(page)
    den, mesiac, rok = helper.aktualny_datum()
    prihlaskaRiad.click_on_pridaj_prihlasku()
    prihlaskaRiad.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaskaRiad.step_2_SVVP()
    prihlaskaRiad.step_3_vyber_skoly()
    prihlaskaRiad.step_4_ZZ()
    prihlaskaRiad.step_5_prilohy()
    prihlaskaRiad.step_6_ostatne_udaje(den, mesiac, rok)
    prihlaskaRiad.click_on_odoslat_prihlasku()
    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=25000)
    expect(page.locator("#riaditel-home-page")).to_contain_text("Prihlášku pre dieťa ste úspešne pridali.")

@pytest.mark.regression
def test_vyriesenie_konfliktu_na_MS(page: Page, test_data) -> None:
    data = test_data["data"]
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaMS(page)
    konflikt = konfliktMS(page)
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)
    expect(page.locator("#info-panel-red-prihlaska-v-konflikte-riad-zs")).to_contain_text("Táto prihláška je v stave - V konflikte.")
    expect(page.locator("#info-panel-red-prihlaska-v-konflikte-riad-zs")).to_contain_text("Vyzvite zákonného zástupcu na výber jednej verzie.")
    expect(page.locator("#info-panel-red-prihlaska-v-konflikte-riad-zs")).to_contain_text("Následne vyriešte konflikt označením jednej prihlášky ako aktívnej.")
    typPrihlasky = page.locator("#detail-prihlasky-riad-MS-ZS-content").text_content()
    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()
    konflikt.click_on_vyzva_na_vyriesenie_konfliktu()
    expect(page.locator("#vyzva-riesenie-konfliktu-title")).to_contain_text("Výzva na riešenie konfliktu")
    expect(page.locator("body")).to_contain_text("Pre dieťa existuje viac ako jedna prihláška. Vyzvite zákonných zástupcov k výberu jednej prihlášky prostredníctvom emailovej notifikácie.")
    expect(page.locator("body")).to_contain_text("Peter Fodrok")
    expect(page.locator("body")).to_contain_text("Mária Bartošová")
    konflikt.odoslat_vyzvu_na_vyriesenie_konfliktu()

    vyzva_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyzva_konflikt = helper.cleanup_email_text(vyzva_konflikt)
    
    expected = (
    f"Vážený/á pán/pani Peter Fodrok, v systéme bolo zistené, že pre žiaka {data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)} "
    f"boli podané viaceré prihlášky. Riaditeľ školy Materská škola pre AT vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    expected1 = (
    f"Vážený/á pán/pani Mária Bartošová, v systéme bolo zistené, že pre žiaka {data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)} "
    f"boli podané viaceré prihlášky. Riaditeľ školy Materská škola pre AT vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    assert vyzva_konflikt in [expected, expected1]

    expect(page.locator("#duplicitne-prihlasky")).to_contain_text("Riaditeľ školy Materská škola pre AT zaslal výzvu na riešenie konfliktu prihlášok.")
    konflikt.click_on_vyriesenie_konfliktu()
    expect(page.locator("#vyriesit-konflikt-title")).to_contain_text("Vyriešiť konflikt")
    expect(page.locator("body")).to_contain_text("Po označení prihlášky ako aktívnej sa automaticky zneaktívnia všetky duplicitné prihlášky pre toto dieťa na všetkých školách.")
    konflikt.odoslat_vyriesenie_konfliktu("Vyriešenie konfliktu.")
    vyriesenie_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyriesenie_konflikt = helper.cleanup_email_text(vyriesenie_konflikt)
    identifikator1 = helper.inkrementuj_identifikator(identifikator)

    expected = f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte s prihláškou/prihláškami {identifikator}, {identifikator1}. Konflikt bol vyriešený . V systéme bude ďalej evidovaná len prihláška {identifikator}. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    expected1 = f"Vážený/á pán/pani Peter Fodrok, riaditeľ školy Materská škola pre AT vyriešil konflikt viacerých prihlášok podaných pre žiaka {data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)}. Ako aktívna bola označená prihláška s identifikátorom {identifikator}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky boli označené ako “Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete overiť po prihlásení do portálu Elektronické prihlášky: Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."

    assert vyriesenie_konflikt in [expected, expected1]

    expect(page.get_by_role("strong")).to_contain_text("Duplicita prihlášok úspešne vyriešená")
    expect(page.locator("#info-panel-green-konflikt-vyrieseny")).to_contain_text("Duplicita prihlášok úspešne vyriešenáVšetky duplicitné prihlášky boli zneaktívnené.")
    expect(page.locator("#info-panel-blue-prihlaska-aktivna")).to_contain_text("Prihláška bola označená ako aktívna riaditeľom školy 910021626 Materská škola pre AT")
    expect(page.locator("#duplicitne-prihlasky")).to_contain_text("Pre dieťa "+data.meno+" "+data.priezvisko+" bol vyriešený konflikt.")
    expect(page.locator("#detail-prihlasky-riad-MS-ZS-content")).to_contain_text("Podaná")
