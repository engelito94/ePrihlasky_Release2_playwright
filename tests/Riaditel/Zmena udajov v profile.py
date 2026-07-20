import pytest
import os
from playwright.sync_api import Page, expect
from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.login_page import LoginPage
from pages.profil_page import ProfilPage

username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_zmena_udajov_riaditela(page: Page, email_account_picker) -> None:
    login = LoginPage(page)
    profil = ProfilPage(page)
    helper = Helper()
    mail = Mail()
    cislo = helper.vygeneruj_tel_cislo()

    login.login_as_riaditel(username, password, "910021626")
    profil.click_on_profil()

    povodny_email = profil.get_email_riaditela()
    profil.click_on_upravit_udaje()
    profil.change_tel_cislo(cislo)

    expect(
        page.locator("#profil-nastavenieRiaditela"),
        "Zmena telefónneho čísla sa neuložila správne."
    ).to_contain_text("Zmeny sme úspešne uložili.")

    page.get_by_role("button", name="Zmeniť e-mail").click()

    account = email_account_picker(povodny_email)
    profil.change_email(account["new_email"])

    kod = mail.get_six_digit_number_from_last_email(
        "imap.gmail.com",
        account["mail_user"],
        account["mail_pw"]
    )
    profil.load_kod(kod)

    expect(
        page.locator("#profil-nastavenieRiaditela"),
        "Zmena e-mailovej adresy sa nepodarila."
    ).to_contain_text("Vašu emailovú adresu sme úspešne zmenili.")

    profil.click_on_profil()

    expect(
        page.locator("#profil-riaditel-skola"),
        "Názov školy v profile sa nezobrazuje správne."
    ).to_contain_text("Materská škola pre AT")

    expect(
        page.locator("#profil-riaditel-tel"),
        "Telefónne číslo v profile sa nezhoduje s očakávanou hodnotou."
    ).to_contain_text(cislo)

    expect(
        page.locator("#profil-meno"),
        "Meno používateľa v profile sa nezobrazuje správne."
    ).to_contain_text("930593020")

    expect(
        page.locator("#profil-riaditel-typ"),
        "Typ používateľa v profile sa nezobrazuje správne."
    ).to_contain_text("Riaditeľ")

    expect(
        page.locator("#profil-riaditel-mail"),
        "E-mailová adresa v profile sa nezhoduje s novou adresou."
    ).to_contain_text(account["mail_user"])

    expect(
        page.locator("#meno-osoby"),
        "Meno osoby v profile sa nezobrazuje správne."
    ).to_contain_text("Peter Fodrok")