import pytest
import os
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.profil_page import ProfilPage

username=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_zmena_skoly_profil_riaditela(page: Page) -> None:
    login = LoginPage(page)
    profil = ProfilPage(page)

    login.login_as_riaditel(username,password,"910021626")
    profil.click_on_profil()
    expect(page.locator("#profil-riaditel-skola")).to_contain_text("Materská škola pre AT")
    page.get_by_role("textbox", name="Škola *").click()
    page.get_by_text("Stredná škola pre AT").click()
    page.get_by_role("button", name="Zmeniť školu").click()
    expect(page.locator("#profil-riaditel-skola")).to_contain_text("Stredná škola pre AT")
    expect(page.get_by_role("banner")).to_contain_text("Stredná škola pre AT — EDUID 910021624")
    page.get_by_role("textbox", name="Škola *").click()
    page.get_by_text("Základná škola pre AT").click()
    page.get_by_role("button", name="Zmeniť školu").click()
    expect(page.locator("#profil-riaditel-skola")).to_contain_text("Základná škola pre AT")
    expect(page.get_by_role("banner")).to_contain_text("Základná škola pre AT — EDUID 910021625")

    
