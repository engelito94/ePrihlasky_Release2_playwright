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
from pages.prilohy_SS_page import PrilohySS

mailuser=os.getenv("GMAIL_USERNAME")
mailpw=os.getenv("GMAIL_APP_PASSWORD")
username=os.getenv("EPRIHLASKY_ZZ_USERNAME")
password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")

#get_by_role("button", name="Stredná škola pre AT Pridať").nth(4)

@pytest.mark.regression
def test_prihlaska_na_SS_2_kolo(page: Page) -> None:
    data = Data.pop_random_person_from_file("./data/detiSS.txt")
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
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
    #step9
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(re.compile(r"P-2026-.+"))
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("2026/2027")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("-")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("2. kolo")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.meno)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.priezvisko)
    expect(page.locator("#suhrnny-prehlad")).to_contain_text(data.priezvisko)
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
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Narcisová 4/2048, 03845, Myjava, Slovenská republika")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Nie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Nie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Nie")
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("ŠVVP")
    expect(page.locator("#skoly")).to_contain_text("1 Stredná škola č. 1")
    expect(page.locator("#skoly")).to_contain_text("910021624")
    expect(page.locator("#skoly")).to_contain_text("Stredná škola pre AT")
    expect(page.locator("#skoly")).to_contain_text("2285H00")
    expect(page.locator("#skoly")).to_contain_text("zlievač -3 ročné")
    expect(page.locator("#skoly")).to_contain_text("Netalentový")
    expect(page.locator("#skoly")).to_contain_text("1. termín")
    expect(page.locator("#skoly")).to_contain_text("slovenský")
    expect(page.locator("#skoly")).to_contain_text("Nie")
    expect(page.locator("#skoly")).to_contain_text("Nie")
    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 1")
    expect(page.locator("#zastupcovia")).to_contain_text("Mária")
    expect(page.locator("#zastupcovia")).to_contain_text("Bartošová")
    expect(page.locator("#zastupcovia")).to_contain_text("-")
    expect(page.locator("#zastupcovia")).to_contain_text("855215/3830")
    expect(page.locator("#zastupcovia")).to_contain_text("15.02.1985")
    expect(page.locator("#zastupcovia")).to_contain_text("Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika")
    expect(page.locator("#zastupcovia")).to_contain_text("katalontest987@gmail.com")
    expect(page.locator("#zastupcovia")).to_contain_text("+421999888777")
    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 2")
    expect(page.locator("#zastupcovia")).to_contain_text("Druhý zákonný zástupca nie je známy.")
    expect(page.locator("#info-o-zs")).to_contain_text("Informácie o základnej škole")
    expect(page.locator("#info-o-zs")).to_contain_text("Zo školy v zahraničí")
    expect(page.locator("#info-o-zs")).to_contain_text("9.")
    expect(page.locator("#info-o-zs")).to_contain_text("9")
    expect(page.locator("#info-o-zs")).to_contain_text("Francúzsky")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("6. ročník (2. polrok)")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("uspokojivé")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("1 - výborný")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("7. ročník (2. polrok)")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("menej uspokojivé")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("3 - dobrý")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("8. ročník (2. polrok)")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("veľmi dobré")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("2 - chválitebný")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("9. ročník (1. polrok)")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("veľmi dobré")
    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_contain_text("1 - výborný")
    expect(page.locator("#sutaze-suhrn")).to_contain_text("Zumba")
    expect(page.locator("#sutaze-suhrn")).to_contain_text("1. miesto - Školská úroveň")
    expect(page.locator("#sutaze-suhrn")).to_contain_text("Umelecké")
    expect(page.locator("#sutaze-suhrn")).to_contain_text("Školský rok: 2023/2024")
    expect(page.locator(".prilohaItem").first).to_be_visible()
    expect(page.locator("#prilohyContainer > div:nth-child(2)")).to_be_visible()
    expect(page.locator("#prilohyContainer > div:nth-child(3)")).to_be_visible()
    expect(page.locator("#prilohyContainer > div:nth-child(4)")).to_be_visible()
    expect(page.locator("#prilohyContainer > div:nth-child(5)")).to_be_visible()
    expect(page.locator("#layoutDorucenie")).to_contain_text("Rozhodnutia o prijatí budú zverejnené na elektronickej výveske, o čom budete informovaný e-mailovou správou.")
    prihlaska.click_on_odoslat_prihlasku()
    expect(page.locator("body")).to_contain_text("Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške. Po odoslaní prihlášky už nebude možné upravovať údaje ani prílohy, pokiaľ vás na opravu nevyzve riaditeľ školy. Pred odoslaním si preto dôkladne skontrolujte všetky údaje a priložené dokumenty. Odoslaním prihlášky sa formálne začne proces jej posúdenia podľa zákona č. 71/1967 Zb. o správnom konaní (správny poriadok).")
    prihlaska.click_on_potvrdit_odoslanie()
    expect(page).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=35000)
    expect(page.locator("h1")).to_contain_text("Prihláška bola úspešne odoslaná!")
    identifikator = page.get_by_text("P-2026-").text_content()
    prihlaska.click_on_prejst_na_prihlasky()
    expect(page).to_have_url(re.compile(r".*/Prihlasky.*"), timeout=35000)
    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021624")
    prihlaska.vyhladanie_prihlasky(data.meno, data.priezvisko)
    expect(page.get_by_text(data.priezvisko+" "+data.meno, exact=True)).to_be_visible()
    expect(page.get_by_text(identifikator, exact=True)).to_be_visible()
    expect(page.locator("div[class='sub-container'] div[class='scrollable-middle-area'] div:nth-child(2) div:nth-child(1) div:nth-child(1)")).to_contain_text("V spracovaní")

@pytest.mark.regression
def test_doplnenie_prilohy_na_SS_2_kolo(page: Page) -> None:
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    priloha = PrilohySS(page)
    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_poslednu_prihlasku()
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Elektronicky")
    meno = page.locator("#dietaMeno").text_content()
    priezvisko = page.locator("#dietaPriezvisko").text_content()
    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()
    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()
    expect(page.locator("#message-box")).to_contain_text("Žiadosť o doplnenie prílohy bola úspešne odoslaná")
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Neúplná")
    expect(page.locator("#skoly")).to_contain_text("Riaditeľ školy Stredná škola pre AT požadoval ďalšie prílohy.")
    expect(page.locator("#skoly")).to_contain_text("Čestné vyhlásenie zákonného zástupcu")
    expect(page.locator("#skoly")).to_contain_text("Žiadam o úpravu alebo doplnenie príloh v prihláške na školu. Detaily v sprievodnom texte: Žiadosť o doplnenie prílohy.")
    priloha.odvolanie_ziadosti()

    odvolanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    odvolanie_prilohy = helper.cleanup_email_text(odvolanie_prilohy)
    expected = f"Vážený/á pán/pani Mária Bartošová, radi by sme vás informovali, že požiadavka na doloženie dodatočných dokumentov príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl bola zrušená. Nie je teda potrebné dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: {meno} {priezvisko} nar. {datum_narodenia} . Ak ste už zadali dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. V prípade akýchkoľvek otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    assert odvolanie_prilohy == expected

    expect(page.locator("#skoly")).to_contain_text("info Výzva odvolaná")
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("V spracovaní")
    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()

    vyziadanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyziadanie_prilohy = helper.cleanup_email_text(vyziadanie_prilohy)
    expected = f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu zlievač pre {meno} {priezvisko} sme zistili, že je potrebné doložiť nasledujúcu prílohu: Čestné vyhlásenie zákonného zástupcu z dôvodu že \" Žiadosť o doplnenie prílohy. \". Prosíme Vás o doplnenie požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu Elektronické prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom odkazu: Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť pridať existujúcu prihlášku do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: {identifikator} Po pridaní prihlášky do konta budete môcť sledovať jej stav, doplniť požadované prílohy a komunikovať so školou. V prípade, že už konto v portáli máte, prihláste sa a pokračujte podľa pokynov v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    assert vyziadanie_prilohy == expected
    
    logout.logout()
    #nahratie prílohy ZZ
    login.login_as_zakonny_zastupca(username, password)
    expect(page.locator("#moje-prihlasky")).to_contain_text("Nahrajte prílohy")
    expect(page.locator("#moje-prihlasky")).to_contain_text("Nahrajte prílohyRiaditeľ strednej školy požaduje doplnenie príloh. Pridanie prílohy nájdete v stĺpci Akcia.")
    priloha.nahrat_prilohu()
    expect(page.locator("#pridat-prilohy")).to_contain_text("Dokumenty ste úspešne nahrali")
    expect(page.locator("#pridat-prilohy")).to_contain_text("Vaša prihláška bude čoskoro posúdená. Ďakujeme za trpezlivosť.")

    prijatie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    prijatie_prilohy = helper.cleanup_email_text(prijatie_prilohy)
    expected = (f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške do Stredná škola pre AT zlievač pre {meno} {priezvisko}, zaevidovanej v elektronickom portáli prihlášok bola doručená príloha s názvom Čestné vyhlásenie zákonného zástupcu. Doručenú prílohu si prosím starostlivo skontrolujte prihlásením sa na portáli Elektronických prihlášok v detaile prihlášky, alebo v prílohe tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave Vašej prihlášky a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\"")
    assert prijatie_prilohy == expected

    priloha.click_on_prejst_na_prihlasky()
    expect(page.locator("#moje-prihlasky")).to_contain_text("Doplnená")
    logout.logout()
    #kontrola na SŠ
    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_prihlasku_po_nahrati_prilohy(meno, priezvisko)
    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Doplnená")
    expect(page.get_by_text("Priložené dokumenty:")).to_be_visible()
