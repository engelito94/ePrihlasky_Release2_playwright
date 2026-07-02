import pytest
import os
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.sprava_pouzivatelov_page import SpravaPouzivatelov

riad_username=os.getenv("EPRIHLASKY_SEC_RIADITEL_USERNAME")
riad_password=os.getenv("EPRIHLASKY_SEC_RIADITEL_PASSWORD")
admin_username=os.getenv("EPRIHLASKY_ADMIN_USERNAME")
admin_password=os.getenv("EPRIHLASKY_ADMIN_PASSWORD")
spracovatel_username=os.getenv("EPRIHLASKY_SPRACOVATEL_USERNAME")
spracovatel_password=os.getenv("EPRIHLASKY_SPRACOVATEL_PASSWORD")

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_pridaj_rolu(page: Page) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    role = SpravaPouzivatelov(page)
    login.login_as_riaditel(riad_username, riad_password, "910020859")
    role.otvor_spravu_pouzivatelov()
    role.click_on_pridat_pouzivatela()
    expect(page.locator("#sprava-pouzivatelov")).to_contain_text("Pridať používateľa")
    expect(page.locator("#sprava-pouzivatelov")).to_contain_text("Vyhľadajte a zapojte odborníkov z vašej školy do procesu kontroly prihlášok.")
    role.pridaj_rolu("930593021", "spracovatel")
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Používateľa ste úspešne pridali.")
    expect(page.locator("#sprava-pouzivatelov")).to_contain_text("Správa používateľov")
    expect(page.get_by_role("paragraph")).to_contain_text("Spravujte používateľov a priraďte im rolu.")
    role.click_on_pridat_pouzivatela()
    role.pridaj_rolu("930593019", "admin")
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Používateľa ste úspešne pridali.")
    logout.logout()
    login.login_as_rola(spracovatel_username, spracovatel_password)
    role.otvor_profil()
    expect(page.locator("#meno-osoby")).to_contain_text("Klaudia Kelmová")
    expect(page.locator("#profil-riaditel-typ")).to_contain_text("Spracovateľ")
    logout.logout()
    login.login_as_rola(admin_username, admin_password)
    role.otvor_profil()
    expect(page.locator("#meno-osoby")).to_contain_text("Dušan Lemo")
    expect(page.locator("#profil-riaditel-typ")).to_contain_text("Administrátor")

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_odstran_rolu(page: Page) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    role = SpravaPouzivatelov(page)
    login.login_as_riaditel(riad_username, riad_password, "910020859")
    role.otvor_spravu_pouzivatelov()
    role.click_on_odstranit()
    expect(page.locator("body")).to_contain_text("Odstránenie údajov")
    role.click_on_potvrdit_odstranenie()
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Používateľa ste úspešne odstránili.")
    role.click_on_odstranit()
    expect(page.locator("body")).to_contain_text("Odstránenie údajov")
    role.click_on_potvrdit_odstranenie()
    expect(page.locator("#sprava-skoly-content")).to_contain_text("Používateľa ste úspešne odstránili.")
    logout.logout()
    login.login_as_rola(admin_username, admin_password)
    expect(page.locator("#error-summary-title-login")).to_contain_text("Neúspešné prihlásenie do systému")
    expect(page.locator("#error-message-login")).to_contain_text("Ľutujeme, ale nemáte priradenú rolu. Ak sa ako zamestnanec školy prihlasujete do portálu, je potrebné aby vám riaditeľ školy v portáli ePrihlášky priradil rolu v rámci správy školy (správa používateľov) - bez priradenej role nie je možné spracovávať prihlášky.")
    login.login_as_rola(spracovatel_username, spracovatel_password)
    expect(page.locator("#error-summary-title-login")).to_contain_text("Neúspešné prihlásenie do systému")
    expect(page.locator("#error-message-login")).to_contain_text("Ľutujeme, ale nemáte priradenú rolu. Ak sa ako zamestnanec školy prihlasujete do portálu, je potrebné aby vám riaditeľ školy v portáli ePrihlášky priradil rolu v rámci správy školy (správa používateľov) - bez priradenej role nie je možné spracovávať prihlášky.")
    