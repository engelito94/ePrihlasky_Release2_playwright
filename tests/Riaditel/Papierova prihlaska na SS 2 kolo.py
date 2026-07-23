import os
import re
import pytest
import utils.data_helper as Data

from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.papierova_prihlaska_SS_page import PapierovaPrihlaskaSS


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _expect_summary_header(page: Page, den: str, mesiac: str, rok: str) -> None:
    _expect_text(page.locator("#ziadostIdentifikator"), "-", "V súhrne chýba identifikátor žiadosti.")
    _expect_text(page.locator("#ziadostSkolskyRok"), "2026 / 2027", "V súhrne chýba školský rok.")
    _expect_text(
        page.locator("#ziadostDatumPodania"),
        f"{den}.{mesiac}.{rok}",
        "V súhrne chýba dátum podania žiadosti."
    )
    _expect_text(page.locator("#ziadostSposobPodania"), "-", "V súhrne chýba spôsob podania.")
    _expect_text(page.locator("#poznamkaSkoly"), "*-*", "V súhrne chýba poznámka školy.")
    _expect_text(page.locator("#koloPrijimaciehoKonania"), "2. kolo", "V súhrne chýba kolo prijímacieho konania.")


def _expect_summary_child(page: Page, data, helper: Helper) -> None:
    _expect_text(page.locator("#dietaMenoSuhrn"), data.meno, "V súhrne chýba meno dieťaťa.")
    _expect_text(page.locator("#dietaPriezviskoSuhrn"), data.priezvisko, "V súhrne chýba priezvisko dieťaťa.")
    _expect_text(
        page.locator("#dietaRodnePriezviskoSuhrn"),
        data.priezvisko,
        "V súhrne chýba rodné priezvisko dieťaťa."
    )
    _expect_text(page.locator("#dietaRodneCisloSuhrn"), data.rodne_cislo, "V súhrne chýba rodné číslo dieťaťa.")
    _expect_text(
        page.locator("#dietaDatumNarodeniaSuhrn"),
        helper.rc_to_datum_narodenia(data.rodne_cislo),
        "V súhrne chýba dátum narodenia dieťaťa."
    )
    _expect_text(
        page.locator("#dietaPohlavieSuhrn"),
        helper.get_pohlavie(data.rodne_cislo),
        "V súhrne chýba pohlavie dieťaťa."
    )
    _expect_text(page.locator("#dietaMiestonarodeniaSuhrn"), "Slovensko", "V súhrne chýba miesto narodenia.")
    _expect_text(page.locator("#dietaNarodnostSuhrn"), "slovenská", "V súhrne chýba národnosť.")
    _expect_text(
        page.locator("#dietaStatnaPrislusnostSuhrn"),
        "Slovenská republika",
        "V súhrne chýba štátna príslušnosť."
    )
    _expect_text(page.locator("#dietaMaterinskyJazykSuhrn"), "slovenský", "V súhrne chýba materinský jazyk.")
    _expect_text(page.locator("#dietaInyMaterinskyJazykSuhrn"), "-", "V súhrne chýba hodnota iného materinského jazyka.")
    _expect_text(
        page.locator("#dietaAdresaTrvalehoPobytuSuhrn"),
        "Korčekova 12/45, 89516, Palín, Slovenská republika",
        "V súhrne chýba adresa trvalého pobytu dieťaťa."
    )


def _expect_summary_svvp(page: Page) -> None:
    _expect_text(page.locator("#dpZmenenaPracovnaSchopnost"), "Nie", "V súhrne chýba údaj o zmene pracovnej schopnosti.")
    _expect_text(page.locator("#dpSVVP"), "Nie", "V súhrne chýba údaj o ŠVVP.")
    _expect_text(page.locator("#dpMentalnePostihnutie"), "Nie", "V súhrne chýba údaj o mentálnom postihnutí.")
    _expect_text(page.locator("#dpPoznamka"), "-_-", "V súhrne chýba poznámka k ŠVVP.")


def _expect_summary_school(page: Page) -> None:
    school = page.locator("#skoly")
    _expect_text(school, "910021624", "V sekcii školy chýba EDUID školy.")
    _expect_text(school, "Stredná škola pre AT", "V sekcii školy chýba názov školy.")
    _expect_text(school, "zlievač -3 ročné", "V sekcii školy chýba študijný odbor.")
    _expect_text(school, "Netalentový", "V sekcii školy chýba typ odboru.")
    _expect_text(school, "1. termín", "V sekcii školy chýba termín skúšky.")
    _expect_text(school, "slovenský", "V sekcii školy chýba vyučovací jazyk.")
    _expect_text(school, "1 Stredná škola č. 1", "V sekcii školy chýba poradie školy.")


def _expect_summary_guardian(page: Page) -> None:
    guardians = page.locator("#zastupcovia")

    _expect_text(guardians, "Osobné údaje zákonného zástupcu č. 1", "V sekcii zástupcov chýba hlavička 1. zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaMeno"), "Demeter", "V sekcii zástupcov chýba meno zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaPriezvisko"), "Varga", "V sekcii zástupcov chýba priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodnePriezvisko"), "-", "V sekcii zástupcov chýba rodné priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodneCislo"), "840303/7269", "V sekcii zástupcov chýba rodné číslo zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaDatumNarodenia"), "03.03.1984", "V sekcii zástupcov chýba dátum narodenia zákonného zástupcu.")
    _expect_text(
        page.locator("#zakonnyZastupcaAdresaBydliska"),
        "Korčekova 12/45, 89516, Palín, Slovenská republika",
        "V sekcii zástupcov chýba adresa zákonného zástupcu."
    )
    _expect_text(page.locator("#zakonnyZastupcaEmail"), "katalontest987@gmail.com", "V sekcii zástupcov chýba e-mail zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaTelefon"), "+421963258741", "V sekcii zástupcov chýba telefón zákonného zástupcu.")

    _expect_text(guardians, "Osobné údaje zákonného zástupcu č. 2", "V sekcii zástupcov chýba hlavička 2. zákonného zástupcu.")
    _expect_text(guardians, "Druhý zákonný zástupca nie je známy.", "V sekcii zástupcov chýba informácia o neznámom 2. zástupcovi.")


def _expect_summary_primary_school(page: Page) -> None:
    _expect_text(page.locator("#prichodZiakaSuhrnZiadost"), "Zo ZŠ na Slovensku", "V súhrne chýba údaj o pôvode žiaka.")
    _expect_text(page.locator("#eduidZSSuhrnZiadost"), "910021625", "V súhrne chýba EDUID základnej školy.")
    _expect_text(page.locator("#nazovZSSuhrnZiadost"), "Základná škola pre AT", "V súhrne chýba názov základnej školy.")
    _expect_text(page.locator("#rocnikSuhrnZiadost"), "9.", "V súhrne chýba ročník žiaka.")
    _expect_text(page.locator("#triedaSuhrnZiadost"), "9.A", "V súhrne chýba trieda žiaka.")
    _expect_text(page.locator("#rokSkolskejDochadzkySuhrnZiadost"), "9", "V súhrne chýba rok školskej dochádzky.")
    _expect_text(page.locator("#vyucovaciJazykVZSSuhrnZiadost"), "Slovenský", "V súhrne chýba vyučovací jazyk ZŠ.")


def _expect_summary_results_and_competitions(page: Page) -> None:
    _expect_text(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "6.ročník (2. polrok) Správanie veľmi dobré 7.ročník (2. polrok) Správanie uspokojivé 8.ročník (2. polrok) Správanie menej uspokojivé 9.ročník (1. polrok) Správanie veľmi dobré",
        "V súhrne chýbajú výsledky vzdelávania."
    )

    competitions = page.locator("#sutaze-suhrn")
    _expect_text(competitions, "Súťaž", "V súhrne chýba sekcia súťaží.")
    _expect_text(competitions, "Preteky v kosení", "V súhrne chýba názov súťaže.")
    _expect_text(competitions, "2. miesto - Krajská úroveň", "V súhrne chýba umiestnenie v súťaži.")
    _expect_text(competitions, "Súťaže zručnosti", "V súhrne chýba kategória súťaže.")
    _expect_text(competitions, "Školský rok: 2024/2025", "V súhrne chýba školský rok súťaže.")


@pytest.mark.regres2kolo
def test_pridanie_papierovej_prihlasky_SS(page: Page) -> None:
    data = Data.generate_unique_person(min_age=15, max_age=17)
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaSS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username, password, "910021624")

    prihlaska.click_on_pridaj_prihlasku()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly()
    prihlaska.step_4_ZZ()
    prihlaska.step_5_navsteva_ZS()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()
    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)

    _expect_summary_header(page, den, mesiac, rok)
    _expect_summary_child(page, data, helper)
    _expect_summary_svvp(page)
    _expect_summary_school(page)
    _expect_summary_guardian(page)
    _expect_summary_primary_school(page)
    _expect_summary_results_and_competitions(page)
    _expect_visible(page.locator(".prilohaItem"), "V súhrne sa nezobrazuje príloha.")

    prihlaska.click_on_odoslat_prihlasku()

    _expect_url(
        page,
        r".*/Riaditel.*",
        "Po odoslaní papierovej prihlášky sa nevrátila stránka riaditeľa."
    )
    _expect_text(
        page.locator("#riaditel-home-page"),
        "Prihlášku pre dieťa ste úspešne pridali.",
        "Po odoslaní papierovej prihlášky sa nezobrazila úspešná hláška."
    )

    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)

    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        f"{data.priezvisko} {data.meno}",
        "V zozname prihlášok sa nezobrazuje meno a priezvisko dieťaťa."
    )
    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        "V spracovaní",
        "V zozname prihlášok chýba stav 'V spracovaní'."
    )

    prihlaska.click_on_zobrazit_prihlasku()

    detail = page.locator("#detail-prihlasky-riad-SS-content")
    _expect_text(detail, "Papierovo", "V detaile prihlášky chýba spôsob podania 'Papierovo'.")
    _expect_text(detail, "2. kolo", "V detaile prihlášky chýba údaj o 2. kole.")