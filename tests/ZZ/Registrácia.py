import pytest
import os
import re
import utils.data_helper as Data
from utils.api_register import MailTmClient
from playwright.sync_api import Page, expect, Playwright
from pages.login_page import LoginPage
from pages.registracia_page import Registracia

user_password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")

@pytest.mark.regression
def test_registracia(page: Page, playwright: Playwright) -> None:
    registracia = Registracia(page)
    login = LoginPage(page)
    mail_client = MailTmClient(playwright)
    email, token = mail_client.create_temp_mailbox()
    data = Data.pop_random_person_from_file("./data/osoba.txt")
    registracia.click_on_registracia()
    expect(page.locator("#step-1")).to_contain_text("Registrácia")
    expect(page.locator("#step-1-panel-container")).to_contain_text("Registráciu vytvára zákonný zástupca dieťaťaPri registrácii vyplňte údaje zákonného zástupcu (nie dieťaťa), ktorý bude prihlášku podávať.")
    registracia.vypln_registracny_formular(email, user_password, data.meno, data.priezvisko, data.rodne_cislo, data.text)
    expect(page.locator("#potvrdenie-registracie")).to_contain_text("Potvrdenie registrácie")
    activation_url = mail_client.wait_for_registration_link(token, timeout_seconds=60)
    page.goto(activation_url)
    page.wait_for_timeout(80000)
    login.login_po_registracii(email, user_password)