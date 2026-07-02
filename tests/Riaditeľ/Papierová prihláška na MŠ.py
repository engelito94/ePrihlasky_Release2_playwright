import pytest
import os
import re
import utils.data_helper as Data
from utils.helpers import Helper
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.papierova_prihlaska_MS_page import PapierovaPrihlaskaMS


username=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_pridanie_papierovej_prihlasky_MS(page: Page) -> None:
    data = Data.pop_random_person_from_file("./data/detiMS.txt")
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaMS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()
    login.login_as_riaditel(username,password,"910021626")
    prihlaska.click_on_pridaj_prihlasku()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly()
    prihlaska.step_4_ZZ()
    prihlaska.step_5_prilohy()
    prihlaska.step_6_ostatne_udaje(den, mesiac, rok)
    #suhrnny prehlad
    expect(page.locator("#suhrnny-prehlad")).to_contain_text("Súhrnný prehľad")
    expect(page.locator("#ziadostSkolskyRok")).to_contain_text("2026 / 2027")
    expect(page.locator("#ziadostDatumPodania")).to_contain_text(den+"."+mesiac+"."+rok)
    expect(page.locator("#poznamkaSkoly")).to_contain_text(":)")
    expect(page.locator("#ziadostIdentifikator")).to_contain_text("-")
    expect(page.locator("#ziadostSposobPodania")).to_contain_text("-")
    expect(page.locator("#dietaMenoSuhrn")).to_contain_text(data.meno)
    expect(page.locator("#dietaPriezviskoSuhrn")).to_contain_text(data.priezvisko)
    expect(page.locator("#dietaRodnePriezviskoSuhrn")).to_contain_text(data.priezvisko)
    expect(page.locator("#dietaRodneCisloSuhrn")).to_contain_text(data.rodne_cislo)
    expect(page.locator("#dietaDatumNarodeniaSuhrn")).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))
    expect(page.locator("#dietaPohlavieSuhrn")).to_contain_text(helper.get_pohlavie(data.rodne_cislo))
    expect(page.locator("#dietaMiestonarodeniaSuhrn")).to_contain_text("Slovensko")
    expect(page.locator("#dietaNarodnostSuhrn")).to_contain_text("slovenská")
    expect(page.locator("#dietaStatnaPrislusnostSuhrn")).to_contain_text("Slovenská republika")
    expect(page.locator("#dietaMaterinskyJazykSuhrn")).to_contain_text("slovenský")
    expect(page.locator("#dietaInyMaterinskyJazykSuhrn")).to_contain_text("-")
    expect(page.locator("#dietaAdresaTrvalehoPobytuSuhrn")).to_contain_text("Miksáthova 8/635, 02845, Kordíky, Slovenská republika")
    expect(page.locator("#dietaAdresaObvyklehoPobytuSuhrn")).to_contain_text("Miksáthova 8/635, 02845, Kordíky, Slovenská republika")
    expect(page.locator("#dpDietataMsCelodennaVychova")).to_contain_text("Celodennú výchovu a vzdelávanie")
    expect(page.locator("#dpDietataSVVPotreby")).to_contain_text("Nie")
    expect(page.locator("#dpDietataSVVPotrebySNadanim")).to_contain_text("Nie")
    expect(page.locator("#dpPozadovanyDatumPrijatia")).to_contain_text("01.09.2026")
    expect(page.locator("#dpDietataPoznamka")).to_contain_text("-")
    expect(page.locator("#skoly")).to_contain_text("1 Materská škola č. 1")
    expect(page.locator("#skoly")).to_contain_text("Materská škola pre AT")
    expect(page.locator("#skoly")).to_contain_text("Balková 98/8, 36578 Banská Bystrica")
    expect(page.locator("#skoly")).to_contain_text("slovenský")
    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 1")
    expect(page.locator("#zakonnyZastupcaMeno")).to_contain_text("Peter")
    expect(page.locator("#zakonnyZastupcaPriezvisko")).to_contain_text("Fodrok")
    expect(page.locator("#zakonnyZastupcaRodnePriezvisko")).to_contain_text("-")
    expect(page.locator("#zakonnyZastupcaRodneCislo")).to_contain_text("860201/7842")
    expect(page.locator("#zastupcovia")).to_contain_text("-")
    expect(page.locator("#zakonnyZastupcaDatumNarodenia")).to_contain_text("01.02.1986")
    expect(page.locator("#zakonnyZastupcaAdresaBydliska")).to_contain_text("Miksáthova 8/635, 02845, Kordíky, Slovenská republika")
    expect(page.locator("#zakonnyZastupcaEmail")).to_contain_text("katalontest987@gmail.com")
    expect(page.locator("#zakonnyZastupcaTelefon")).to_contain_text("+421905866541")
    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 2")
    expect(page.locator("#zastupcovia")).to_contain_text("Druhý zákonný zástupca nie je známy.")
    expect(page.locator("#prilohyHederText")).to_contain_text("Prílohy")
    expect(page.locator(".prilohaItem")).to_be_visible()
    #odoslanie prihlášky
    prihlaska.click_on_odoslat_prihlasku()
    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=25000)
    expect(page.locator("#riaditel-home-page")).to_contain_text("Prihlášku pre dieťa ste úspešne pridali.")
    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)
    expect(page.get_by_text("P-2026-")).to_be_visible()
    expect(page.get_by_text("Podaná").first).to_be_visible()
    expect(page.get_by_text("Papierovo")).to_be_visible()
