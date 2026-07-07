import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.odbory_page import Odbory

riad_username=os.getenv("EPRIHLASKY_SEC_RIADITEL_USERNAME")
riad_password=os.getenv("EPRIHLASKY_SEC_RIADITEL_PASSWORD")

@pytest.mark.regres2kolo
def test_otvorenie_a_vymazanie_odboru_2_kolo(page: Page) -> None:
    login = LoginPage(page)
    odbor = Odbory(page)
    login.login_as_riaditel(riad_username, riad_password, "910020859")
    odbor.click_on_menu_odbory()
    expect(page.locator("#riaditel-odbory-pre-2-kolo")).to_contain_text("Odbory pre 2. kolo")
    expect(page.locator("#riaditel-odbory-pre-2-kolo")).to_contain_text("Pridajte odbory, pre ktoré chcete otvoriť 2. kolo.")
    odbor.click_on_otvorit_odbor()
    expect(page.locator("#odbory-a-kriteria-content")).to_contain_text("Otvoriť odbor pre 2. kolo")
    expect(page.locator("#odbory-a-kriteria-content")).to_contain_text("Vyberte odbor a zadajte počet voľných miest, ktoré chcete ponúknuť v 2. kole prijímacieho konania pre tento odbor.(Počet nesmie prekročiť rozdiel medzi celkovou kapacitou odboru a počtom už prijatých uchádzačov.)")
    odbor.vyber_odbor_kapacitu()
    expect(page.locator("#message-box")).to_contain_text("Odbor pre 2. kolo úspešne pridaný.")
    expect(page.locator("#odbory-message-box")).to_contain_text("Odbory pre 2. kolo nie sú zverejnenéPridajte odbory pre 2. kolo a následne ich zverejnite.")
    odbor.click_on_zverejnit_odbor()
    expect(page.locator("body")).to_contain_text("Zverejnenie odborov")
    expect(page.locator("body")).to_contain_text("Chystáte sa zverejniť odbory. Zverejnením umožníte podávať prihlášky na odbory. Odbory po zverejnení nebude možné zmeniť.")
    odbor.odstran_odbor()
