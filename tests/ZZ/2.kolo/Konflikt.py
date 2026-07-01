import pytest
import os
import re
import utils.data_helper as Data
from utils.helpers import Helper 
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prihlaska_SS_page import PrihlaskaSS
from pages.papierova_prihlaska_SS_page import PapierovaPrihlaskaSS
from pages.konflikt_SS_page import KofliktSS


username=os.getenv("EPRIHLASKY_ZZ_USERNAME")
password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")
mailuser=os.getenv("GMAIL_USERNAME")
mailpw=os.getenv("GMAIL_APP_PASSWORD")

#get_by_role("button", name="Stredná škola pre AT Pridať").nth(4)

@pytest.mark.regression
def test_vytvorenie_konfliktu_2_kolo(page: Page) -> None:
    data = Data.pop_random_person_from_file("./data/detiSS.txt")
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaSS(page)
    prihlaskaRiad = PapierovaPrihlaskaSS(page)
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
    prihlaska.click_on_potvrdit_odoslanie()
    expect(page).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=35000)
    #identifikator = page.get_by_text("P-2026-").text_content()
    prihlaska.click_on_prejst_na_prihlasky()
    expect(page).to_have_url(re.compile(r".*/Prihlasky.*"), timeout=35000)
    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021624")
    den, mesiac, rok = helper.aktualny_datum()
    prihlaskaRiad.click_on_pridaj_prihlasku()
    prihlaskaRiad.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaskaRiad.step_2_SVVP()
    prihlaskaRiad.step_3_vyber_skoly()
    prihlaskaRiad.step_4_ZZ()
    prihlaskaRiad.step_5_navsteva_ZS()
    prihlaskaRiad.step_6_znamky()
    prihlaskaRiad.step_7_sutaze()
    prihlaskaRiad.step_8_prilohy()
    prihlaskaRiad.step_9_ostatne_udaje(den, mesiac, rok)
    prihlaskaRiad.click_on_odoslat_prihlasku()
    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=35000)

@pytest.mark.regression
def test_vyriesenie_konfliktu_2_kolo(page: Page) -> None:
    login = LoginPage(page)
    mail = Mail()
    helper = Helper()
    konflikt = KofliktSS(page)
    login.login_as_riaditel(username_riad, password_riad, "910021624")
    konflikt.najdi_prihlasku_v_konflikte()
    expect(page.locator("#info-panel-red-prihlaska-v-konflikte-riad-ss")).to_contain_text("Táto prihláška je v stave - V konflikte.")
    expect(page.locator("#info-panel-red-prihlaska-v-konflikte-riad-ss")).to_contain_text("Táto prihláška je v stave - V konflikte.Pre toto dieťa existuje v systéme viacero prihlášok.Vyzvite zákonného zástupcu na výber jednej verzie.Následne vyriešte konflikt označením jednej prihlášky ako aktívnej.Bez vyriešenia konfliktu nie je možné prihlášku ďalej spracovávať.")

    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Elektronicky")
    meno = page.locator("#dietaMeno").text_content()
    priezvisko = page.locator("#dietaPriezvisko").text_content()
    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("V konflikte")
    konflikt.click_on_vyzva_na_vyriesenie_konfliktu()
    expect(page.locator("body")).to_contain_text("Pre dieťa existuje viac ako jedna prihláška. Vyzvite zákonných zástupcov k výberu jednej prihlášky prostredníctvom emailovej notifikácie.")
    expect(page.locator("body")).to_contain_text("Mária Bartošová")
    expect(page.locator("body")).to_contain_text("Demeter Varga")
    konflikt.click_on_odoslat_vyzvu("Výzva na vyriešenie konfliktu.")
    vyzva_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyzva_konflikt = helper.cleanup_email_text(vyzva_konflikt)
    
    expected = (
    f"Vážený/á pán/pani Demeter Varga, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} nar. {datum_narodenia} "
    f"boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT Vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    expected1 = (
    f"Vážený/á pán/pani Mária Bartošová, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} nar. {datum_narodenia} "
    f"boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT Vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    assert vyzva_konflikt in [expected, expected1]

    expect(page.locator("#duplicitne-prihlasky")).to_contain_text("Riaditeľ školy Stredná škola pre AT zaslal výzvu na riešenie konfliktu prihlášok.")
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("V konflikte")
    konflikt.click_on_vyriesit_konflikt()
    expect(page.locator("#vyriesit-konflikt-title")).to_contain_text("Vyriešiť konflikt")
    expect(page.locator("body")).to_contain_text("Po označení prihlášky ako aktívnej sa automaticky zneaktivnia všetky duplicitné prihlášky pre toto dieťa na všetkých školách.")
    konflikt.click_on_odoslat_konfikt("Vyriešiť konflikt.")
    vyriesenie_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyriesenie_konflikt = helper.cleanup_email_text(vyriesenie_konflikt)
    identifikator1 = helper.inkrementuj_identifikator(identifikator)

    expected = f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte s prihláškou/prihláškami {identifikator}, {identifikator1}. Konflikt bol vyriešený . V systéme bude ďalej evidovaná len prihláška {identifikator}. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    expected1 = f"Vážený/á pán/pani Demeter Varga, riaditeľ školy Stredná škola pre AT vyriešil konflikt viacerých prihlášok podaných pre žiaka {meno} {priezvisko} nar. {datum_narodenia}. Ako aktívna bola označená prihláška s identifikátorom {identifikator}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky boli označené ako “Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete overiť po prihlásení do portálu Elektronické prihlášky: Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."

    assert vyriesenie_konflikt in [expected, expected1]

    expect(page.get_by_role("strong")).to_contain_text("Duplicita prihlášok úspešne vyriešená")
    expect(page.locator("#info-panel-blue-prihlaska-aktivna")).to_contain_text("Prihláška bola označená ako aktívna riaditeľom školy 910021624 Stredná škola pre AT")
    expect(page.locator("#info-panel-blue-prihlaska-aktivna")).to_contain_text("Ak je potrebné označiť inú prihlášku ako aktívnu, kontaktujte riaditeľa uvedenej školy.")
    expect(page.locator("#duplicitne-prihlasky")).to_contain_text("Pre žiaka "+meno+" "+priezvisko+" bol vyriešený konflikt.")
    expect(page.locator("div.stavPrihlasky.badge")).to_contain_text("V spracovaní")
