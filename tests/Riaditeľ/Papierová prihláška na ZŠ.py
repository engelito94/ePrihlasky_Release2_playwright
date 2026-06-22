import pytest
import os
import re
import utils.data_helper as Data
from utils.helpers import Helper
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.papierova_prihlaska_ZS_page import PapierovaPrihlaskaZS


username=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")

@pytest.mark.regression
@pytest.mark.prihlaskaRiaditel
def test_pridanie_papierovej_prihlasky_ZS(page: Page) -> None:
    data = Data.pop_random_person_from_file("./data/detiZS.txt")
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaZS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()
    login.login_as_riaditel(username,password,"910021625")
    prihlaska.click_on_pridaj_prihlasku()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_4_ZZ()
    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)
    #expect(page.locator("#suhrnny-prehlad")).to_contain_text("Identifikátor prihlášky - Školský rok 2026 / 2027 Dátum podania 19.06.2026 Spôsob podania - Poznámka školy Poznámka školy. Kolo prijímacieho konania -")
    #expect(page.locator("#suhrnny-prehlad")).to_contain_text("Meno "+data.meno+" Priezvisko "+data.priezvisko+" Rodné priezvisko - Rodné číslo "+data.rodne_cislo+" Dátum narodenia "+helper.rc_to_datum_narodenia(data.rodne_cislo)+" Pohlavie "+helper.get_pohlavie(data.rodne_cislo)+" Miesto narodenia Slovensko Národnosť slovenská Štátna príslušnosť Slovenská republika Materinský jazyk slovenský Iný materinský jazyk anglický Adresa trvalého pobytu New Dhili, 879/71, Indická republika Adresa miesta, kde sa dieťa obvykle zdržiava, ak je iná, než adresa trvalého pobytu. Viničky 58, 11258, Viničky, Slovenská republika Povinné predprimárne vzdelávanie aktuálne v -")
    expect(page.locator("#pdpDietata")).to_contain_text("Žiadam o prijatie dieťaťa na Požadovaná výchova Etická Záujem o stravovanie v školskej jedálni Áno Záujem o školský klub detí Nie Zdravotné znevýhodnenie dieťaťa Nie Dieťa s nadaním Nie Požadovaný dátum prijatia dieťaťa do materskej školy - Popis znevýhodnenia Popis nadania Poznámka ŠVVP Pokračovanie v plnení povinného predprimárneho vzdelávania - Zmenená pracovná schopnosť - Špeciálne výchovno-vzdelávacie potreby - Mentálne postihnutie - Poznámka -")
    expect(page.locator("#skoly")).to_contain_text("1 Základná škola č. 1 Názov školy Základná škola pre AT Sídlo základnej školy Jalmová 266/19, 06534 Prešov Vzdelávanie dieťaťa žiadam poskytovať v jazyku slovenský Záujem o prípravný ročník Nie Záujem o úvodný ročník Nie")
    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 1 Meno Patrik Priezvisko Kvarga Rodné priezvisko - Rodné číslo 650204/9367 Číslo elektronickej schránky - Dátum narodenia 04.02.1965 Korešpondenčná adresa New Dhili, 879/71, Indická republika E-mail - Telefónne číslo +421966332557 Súhlas s komunikáciou výhradne so zákonným zástupcom č. 1 - Osobné údaje zákonného zástupcu č. 2 Meno - Priezvisko - Rodné priezvisko - Rodné číslo - Číslo elektronickej schránky - Dátum narodenia - Korešpondenčná adresa - E-mail - Telefónne číslo - Čestne vyhlasujem, že s podaním prihlášky súhlasí aj druhý zákonný zástupca dieťaťa - Dôvod, prečo nebolo dané čestné vyhlásenie o súhlase druhého zákonného zástupcu s podaním prihlášky - Druhý zákonný zástupca nie je známy. Názov zariadenia - IČO zariadenia - Adresa zariadenia - Číslo elektronickej schránky - E-mail - Telefónne číslo -")
    expect(page.locator("#prilohyContainer")).to_contain_text("Neboli nahrané žiadne prílohy.")
    prihlaska.click_on_odoslat_prihlasku()
    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=25000)
    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)
    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text(data.priezvisko+" "+data.meno)
    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text("Papierovo")
