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
from pages.prilohy_MS_page import PrilohyMS

mailuser=os.getenv("GMAIL_USERNAME")
mailpw=os.getenv("GMAIL_APP_PASSWORD")
username=os.getenv("EPRIHLASKY_ZZ_USERNAME")
password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")

@pytest.fixture(scope="module")
def test_data():
    data = Data.pop_random_person_from_file("./data/detiMS.txt")

    return {
        "data": data,
    }

@pytest.mark.regression
def test_prihlaska_na_MS(page: Page, test_data) -> None:
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
    #step6 súhrnný prehľad
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(re.compile(r"P-2026-.+"))
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("2026/2027")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.meno)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.priezvisko)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.rodne_cislo)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))
    if helper.get_pohlavie(data.rodne_cislo) == "ženské":
        pohlavie = "žena"
    else:
        pohlavie = "muž"
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(pohlavie)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Slovensko")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("slovenská")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Slovenská republika")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("slovenský")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Debraďská 999/21, 54231, Bobot, Slovenská republika")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Debraďská 999/21, 54231, Bobot, Slovenská republika")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Celodennú výchovu a vzdelávanie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Nie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Nie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("07.09.2026")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("ŠVVP")
    expect(page.locator("#skoly")).to_contain_text("Materská škola pre AT")
    expect(page.locator("#skoly")).to_contain_text("Balková 98/8, 36578 Banská Bystrica")
    expect(page.locator("#skoly")).to_contain_text("slovenský")
    expect(page.locator("#zastupcovia")).to_contain_text("Mária")
    expect(page.locator("#zastupcovia")).to_contain_text("Bartošová")
    expect(page.locator("#zastupcovia")).to_contain_text("-")
    expect(page.locator("#zastupcovia")).to_contain_text("855215/3830")
    expect(page.locator("#zastupcovia")).to_contain_text("15.02.1985")
    expect(page.locator("#zastupcovia")).to_contain_text("Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika")
    expect(page.locator("#zastupcovia")).to_contain_text("katalontest987@gmail.com")
    expect(page.locator("#zastupcovia")).to_contain_text("+421999888777")
    expect(page.locator("#zastupcovia")).to_contain_text("Nie")
    expect(page.locator("#zastupcovia")).to_contain_text("Fero")
    expect(page.locator("#zastupcovia")).to_contain_text("Bartoš")
    expect(page.locator("#zastupcovia")).to_contain_text("-")
    expect(page.locator("#zastupcovia")).to_contain_text("860224/7005")
    expect(page.locator("#zastupcovia")).to_contain_text("24.02.1986")
    expect(page.locator("#zastupcovia")).to_contain_text("Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika")
    expect(page.locator("#zastupcovia")).to_contain_text("mail@tst.net")
    expect(page.locator("#zastupcovia")).to_contain_text("+421954856321")
    expect(page.locator("#zastupcovia")).to_contain_text("Áno")
    expect(page.locator(".prilohaItem").first).to_be_visible()
    prihlaska.odoslat_prihlasku_MS()
    expect(page).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=35000)
    expect(page.locator("h1")).to_contain_text("Prihláška bola úspešne odoslaná!")
    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    expect(page).to_have_url(re.compile(r".*/Riaditel*"), timeout=35000)
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)
    expect(page.locator("#detail-prihlasky-riad-MS-ZS-content")).to_contain_text("Elektronicky")
    expect(page.locator("#detail-prihlasky-riad-MS-ZS-content")).to_contain_text("Podaná")
    expect(page.locator("#dietaMeno")).to_contain_text(data.meno)
    expect(page.locator("#dietaPriezvisko")).to_contain_text(data.priezvisko)
    expect(page.locator("#dietaRodneCislo")).to_contain_text(data.rodne_cislo)


@pytest.mark.regression
def test_doplnenie_prilohy_na_MS(page: Page, test_data) -> None:
    data = test_data["data"]
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaMS(page)
    prilohy = PrilohyMS(page)
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)
    expect(page.locator("#detail-prihlasky-riad-MS-ZS-content")).to_contain_text("Podaná")
    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()
    prilohy.vyziadanie_prilohy_MS()
    prilohy.odvolanie_prilohy_MS()

    odvolanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    odvolanie_prilohy = helper.cleanup_email_text(odvolanie_prilohy)
    expected = f"Vážený/á pán/pani Mária Bartošová, radi by sme vás informovali, že požiadavka na doloženie dodatočných dokumentov príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl bola zrušená. Nie je teda potrebné dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: {data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)} . Ak ste už zadali dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. V prípade akýchkoľvek otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    assert odvolanie_prilohy == expected

    expect(page.locator("#skoly")).to_contain_text("info Výzva odvolaná")
    prilohy.vyziadanie_prilohy_MS()

    vyziadanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyziadanie_prilohy = helper.cleanup_email_text(vyziadanie_prilohy)
    expected = f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu Materská škola pre AT pre {data.meno} {data.priezvisko} sme zistili, že je potrebné doložiť nasledujúcu prílohu: Rozhodnutie súdu z dôvodu že \" Odvolanie prílohy. \". Prosíme Vás o doplnenie požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu Elektronické prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom odkazu: Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť pridať existujúcu prihlášku do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: {identifikator} Po pridaní prihlášky do konta budete môcť sledovať jej stav, doplniť požadované prílohy a komunikovať so školou. V prípade, že už konto v portáli máte, prihláste sa a pokračujte podľa pokynov v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    assert vyziadanie_prilohy == expected

    expect(page.locator("#message-box")).to_contain_text("Žiadosť o doplnenie prílohy bola úspešne odoslaná")
    expect(page.locator("#skoly")).to_contain_text("Riaditeľ školy Materská škola pre AT požadoval ďalšie prílohy.")
    expect(page.locator("#skoly")).to_contain_text("Neúplná")
    
    logout.logout()
    login.login_as_zakonny_zastupca(username, password)

    expect(page.locator("#moje-prihlasky")).to_contain_text("Nahrajte prílohy")
    expect(page.locator("#moje-prihlasky")).to_contain_text("Nahrajte prílohyRiaditeľ materskej školy požaduje doplnenie príloh. Pridanie prílohy nájdete v stĺpci Akcia.")

    prilohy.pridat_prilohu_MS()

    prijatie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    prijatie_prilohy = helper.cleanup_email_text(prijatie_prilohy)
    expected = (f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške do Materská škola pre AT pre {data.meno} {data.priezvisko}, zaevidovanej v elektronickom portáli prihlášok bola doručená príloha s názvom Rozhodnutie súdu. Doručenú prílohu si prosím starostlivo skontrolujte prihlásením sa na portáli Elektronických prihlášok v detaile prihlášky, alebo v prílohe tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave Vašej prihlášky a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\"")
    assert prijatie_prilohy == expected

    expect(page.locator("#pridat-prilohy")).to_contain_text("Dokumenty ste úspešne nahrali")
    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)
    expect(page.locator("#detail-prihlasky-riad-MS-ZS-content")).to_contain_text("Doplnená")
    expect(page.get_by_text("Priložené dokumenty: article")).to_be_visible()
    expect(page.locator("#skoly")).to_contain_text("Doplnená")
