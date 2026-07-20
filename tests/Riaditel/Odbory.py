import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.odbory_page import Odbory


riad_username = os.getenv("EPRIHLASKY_SEC_RIADITEL_USERNAME")
riad_password = os.getenv("EPRIHLASKY_SEC_RIADITEL_PASSWORD")
riad_username1 = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
riad_password1 = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.mark.regres2kolo
def test_otvorenie_a_vymazanie_odboru_2_kolo(page: Page) -> None:
    login = LoginPage(page)
    odbor = Odbory(page)

    login.login_as_riaditel(riad_username, riad_password, "910020859")
    odbor.click_on_menu_odbory()

    expect(
        page.locator("#riaditel-odbory-pre-2-kolo"),
        "Sekcia 'Odbory pre 2. kolo' sa nezobrazila alebo neobsahuje správny nadpis."
    ).to_contain_text("Odbory pre 2. kolo")

    expect(
        page.locator("#riaditel-odbory-pre-2-kolo"),
        "V sekcii odborov pre 2. kolo chýba informačný text o pridaní odborov."
    ).to_contain_text("Pridajte odbory, pre ktoré chcete otvoriť 2. kolo.")

    odbor.click_on_otvorit_odbor()

    expect(
        page.locator("#odbory-a-kriteria-content"),
        "Modal pre otvorenie odboru pre 2. kolo sa nezobrazil."
    ).to_contain_text("Otvoriť odbor pre 2. kolo")

    expect(
        page.locator("#odbory-a-kriteria-content"),
        "V modale pre otvorenie odboru chýba text s inštrukciou o výbere odboru a kapacity."
    ).to_contain_text(
        "Vyberte odbor a zadajte počet voľných miest, ktoré chcete ponúknuť v 2. kole prijímacieho konania pre tento odbor.(Počet nesmie prekročiť rozdiel medzi celkovou kapacitou odboru a počtom už prijatých uchádzačov.)"
    )

    odbor.vyber_odbor_kapacitu()

    expect(
        page.locator("#message-box"),
        "Po pridaní odboru sa nezobrazila úspešná hláška."
    ).to_contain_text("Odbor pre 2. kolo úspešne pridaný.")

    expect(
        page.locator("#odbory-message-box"),
        "Nezobrazila sa informácia, že odbory pre 2. kolo ešte nie sú zverejnené."
    ).to_contain_text(
        "Odbory pre 2. kolo nie sú zverejnenéPridajte odbory pre 2. kolo a následne ich zverejnite."
    )

    odbor.click_on_zverejnit_odbor()

    expect(
        page.locator("body"),
        "Dialóg pre zverejnenie odborov sa nezobrazil."
    ).to_contain_text("Zverejnenie odborov")

    expect(
        page.locator("body"),
        "V dialógu zverejnenia odborov chýba upozornenie o nezmeniteľnosti odborov po zverejnení."
    ).to_contain_text(
        "Chystáte sa zverejniť odbory. Zverejnením umožníte podávať prihlášky na odbory. Odbory po zverejnení nebude možné zmeniť."
    )

    odbor.odstran_odbor()


@pytest.mark.regres1kolo
def test_pridanie_a_vymazanie_odboru_1_kolo(page: Page) -> None:
    login = LoginPage(page)
    odbor = Odbory(page)

    login.login_as_riaditel(riad_username1, riad_password1, "910021685")
    odbor.pridaj_odbor_1_kolo()

    expect(
        page.locator("#message-box"),
        "Po pridaní odboru v 1. kole sa nezobrazila úspešná hláška."
    ).to_contain_text("Odbory boli úspešne pridané")

    odbor.aktualizuj_odbory_1_kolo()

    expect(
        page.locator("#message-box"),
        "Po aktualizácii odboru v 1. kole sa nezobrazila úspešná hláška."
    ).to_contain_text("Odbory boli úspešne aktualizované")

    odbor.odstran_odbor_1_kolo()

    expect(
        page.locator("#riaditel-ziadne-odbory"),
        "Po odstránení odboru sa nezobrazila informácia, že v ročníku nie sú žiadne odbory."
    ).to_contain_text("Žiadne odbory v ročníku")