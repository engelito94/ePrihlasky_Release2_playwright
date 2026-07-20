import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.verejna_zona_page import VerejnaZona
from pages.sprava_skoly_page import SpravaSkoly


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _update_ss_school_profile_first_version(
    page: Page,
    login_page: LoginPage,
    sprava_skoly: SpravaSkoly,
) -> None:
    login_page.login_as_riaditel(username, password, "910021624")
    sprava_skoly.click_on_menu_sprava_skoly()

    page.get_by_label("Úplná debarierizácia všetkých priestorov a vonkajšieho areálu").click()
    page.get_by_label("Bez telocvične").click()
    page.get_by_label("Multifunkčné vonkajšie ihrisko").click()
    page.locator("#radioGroup-SS_DigR_option_0").click()
    page.locator("#radioGroup-SS_WiFi_option_1").check()
    page.get_by_role("textbox", name="Krátky popis školy").fill("testovací popis 1")

    sprava_skoly.click_on_ulozit_zmeny()

    _expect_text(
        page.locator("#sprava-skoly-content"),
        "Údaje profilu školy boli úspešne uložené",
        "Po uložení 1. verzie profilu SS sa nezobrazila úspešná hláška."
    )


def _update_ss_school_profile_second_version(
    page: Page,
    login_page: LoginPage,
    sprava_skoly: SpravaSkoly,
) -> None:
    login_page.login_as_riaditel(username, password, "910021624")
    sprava_skoly.click_on_menu_sprava_skoly()

    page.locator("#radioGroup-SS_DebS_option_1").click()
    page.get_by_label("Viac telocviční").click()
    page.get_by_label("Viaceré multifunkčné vonkajšie ihriská, bežecká dráha").click()
    page.locator("#radioGroup-SS_DigR_option_4").click()
    page.locator("#radioGroup-SS_WiFi_option_0").check()
    page.get_by_role("textbox", name="Krátky popis školy").fill("testovací popis 2")

    sprava_skoly.click_on_ulozit_zmeny()

    _expect_text(
        page.locator("#sprava-skoly-content"),
        "Údaje profilu školy boli úspešne uložené",
        "Po uložení 2. verzie profilu SS sa nezobrazila úspešná hláška."
    )


def _open_public_ss_profile(verejna_zona: VerejnaZona) -> None:
    verejna_zona.vyhladaj_skolu("Stredná škola pre AT", "910021624", "Stredné školy")
    verejna_zona.click_on_profil_skoly()


def _expect_ss_public_profile_first_version(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "Stredná škola pre AT", "Vo verejnom profile chýba názov strednej školy.")
    _expect_text(locator, "Lumpová 11/4, 08796, Žilina", "Vo verejnom profile chýba adresa strednej školy.")
    _expect_text(locator, "testovací popis 1", "Vo verejnom profile chýba prvý testovací popis.")
    _expect_text(
        locator,
        "Úplná debarierizácia všetkých priestorov a vonkajšieho areálu",
        "Vo verejnom profile chýba prvý údaj o debarierizácii."
    )
    _expect_text(locator, "Bez telocvične", "Vo verejnom profile chýba prvý údaj o telocvični.")
    _expect_text(locator, "Multifunkčné vonkajšie ihrisko", "Vo verejnom profile chýba prvý údaj o ihrisku.")
    _expect_text(locator, "Nie", "Vo verejnom profile chýba očakávaná hodnota 'Nie'.")

    _expect_visible(
        page.get_by_text("check").first,
        "Vo verejnom profile sa nezobrazuje prvá ikonka 'check'."
    )
    _expect_visible(
        page.locator("div[class='category'] div:nth-child(3) span:nth-child(1)"),
        "Vo verejnom profile sa nezobrazuje očakávaný indikátor digitálneho vybavenia."
    )
    _expect_visible(
        page.locator("div:nth-child(4) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje 4. ikonka kategórie."
    )
    _expect_visible(
        page.locator("div:nth-child(5) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje 5. ikonka kategórie."
    )
    _expect_visible(
        page.locator("div:nth-child(6) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje 6. ikonka kategórie."
    )


def _expect_ss_public_profile_second_version(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "Stredná škola pre AT", "Vo verejnom profile chýba názov strednej školy po druhej úprave.")
    _expect_text(locator, "testovací popis 2", "Vo verejnom profile chýba druhý testovací popis.")
    _expect_text(locator, "Prístupné prízemie", "Vo verejnom profile chýba druhý údaj o debarierizácii.")
    _expect_text(locator, "Viac telocviční", "Vo verejnom profile chýba druhý údaj o telocvični.")
    _expect_text(
        locator,
        "Viaceré multifunkčné vonkajšie ihriská, bežecká dráha",
        "Vo verejnom profile chýba druhý údaj o ihrisku."
    )
    _expect_text(locator, "Áno", "Vo verejnom profile chýba očakávaná hodnota 'Áno'.")

    _expect_visible(
        page.get_by_text("check").first,
        "Vo verejnom profile sa nezobrazuje prvá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(1),
        "Vo verejnom profile sa nezobrazuje druhá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(2),
        "Vo verejnom profile sa nezobrazuje tretia ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(3),
        "Vo verejnom profile sa nezobrazuje štvrtá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(4),
        "Vo verejnom profile sa nezobrazuje piata ikonka 'check' po druhej úprave."
    )


@pytest.mark.spravaSkoly
@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_profil_skoly_SS(page: Page) -> None:
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)
    verejna_zona = VerejnaZona(page)
    sprava_skoly = SpravaSkoly(page)

    _update_ss_school_profile_first_version(page, login_page, sprava_skoly)
    logout_page.logout()

    _open_public_ss_profile(verejna_zona)
    _expect_ss_public_profile_first_version(page)

    page.locator("button").filter(has_text="Zavrieť").last.click()

    _update_ss_school_profile_second_version(page, login_page, sprava_skoly)
    logout_page.logout()

    _open_public_ss_profile(verejna_zona)
    _expect_ss_public_profile_second_version(page)