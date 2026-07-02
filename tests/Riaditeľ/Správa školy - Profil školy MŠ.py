import os
import re
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.verejna_zona_page import VerejnaZona
from pages.sprava_skoly_page import SpravaSkoly


username=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")

@pytest.mark.spravaSkoly
@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_profil_skoly_MS(page: Page) -> None:
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)
    verejna_zona = VerejnaZona(page)
    sprava_skoly = SpravaSkoly(page)
    login_page.login_as_riaditel(username, password, "910021626")
    sprava_skoly.click_on_menu_sprava_skoly()
    page.get_by_text("Škola neprístupná pre osoby").click()
    page.get_by_text("Telocvičňa do 400 m2").click()
    page.get_by_text("Základné vonkajšie ihrisko").click()
    page.get_by_role("textbox", name="Krátky popis školy *").fill("testovací popis 1")
    sprava_skoly.click_on_ulozit_zmeny()
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Údaje profilu školy boli úspešne uložené")
    logout_page.logout()
    verejna_zona.vyhladaj_skolu("Materská škola pre AT", "910021626", "Materské školy")
    verejna_zona.click_on_profil_skoly()
    expect(page.locator("#najst-skolu-content")).to_contain_text("Materská škola pre AT, Balková 8")
    expect(page.locator("#najst-skolu-content")).to_contain_text("testovací popis 1")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Škola neprístupná pre osoby so zníženou mobilitou")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Telocvičňa do 400 m2")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Základné vonkajšie ihrisko")
    page.get_by_role("button", name="Zavrieť").click()
    login_page.login_as_riaditel(username, password, "910021626")
    sprava_skoly.click_on_menu_sprava_skoly()
    page.get_by_text("Prístupné poschodia, toalety").click()
    page.get_by_text("Viac telocviční").click()
    page.get_by_text("Viaceré multifunkčné vonkajš").click()
    page.get_by_role("textbox", name="Krátky popis školy *").fill("testovací popis 2")
    sprava_skoly.click_on_ulozit_zmeny()
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Údaje profilu školy boli úspešne uložené")
    logout_page.logout()
    verejna_zona.vyhladaj_skolu("Materská škola pre AT", "910021626", "Materské školy")
    verejna_zona.click_on_profil_skoly()
    expect(page.locator("#najst-skolu-content")).to_contain_text("testovací popis 2")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Prístupné poschodia, toalety a jedáleň")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Viac telocviční")
    expect(page.locator("#najst-skolu-content")).to_contain_text("Viaceré multifunkčné vonkajšie ihriská")
