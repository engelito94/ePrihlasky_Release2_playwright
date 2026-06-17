import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.login_link = page.get_by_role("link", name="Prihlásiť sa")
        self.username_input = page.get_by_role("textbox", name="Prihlasovacie meno *")
        self.password_input = page.get_by_role("textbox", name="Heslo *")
        self.submit_button = page.get_by_role("button", name="Prihlásiť sa")
        self.login_form = page.get_by_role("link", name="account_circle Prihlasovacie")

        self.login_link_riad = page.get_by_role("link", name="Pre školy")
        self.school = page.get_by_role("textbox", name="Vybrať školu *")
        self.submit_button_riad = page.get_by_role("button", name="Pokračovať")
        self.name_of_school = page.locator("input.govuk-input.autocomplete-input")

    def open(self):
        self.open_relative("/")

    def _open_login_form(self):
        self.login_link.click()
        self.login_form.click()

    def _open_login_form_riad(self):
        self.login_link_riad.click()

    def _fill_username(self, username: str):
        self.username_input.fill(username)

    def _fill_password(self, password: str):
        self.password_input.fill(password)

    def _click_login_button(self):
        self.submit_button.click()

    def _click_on_school(self):
        self.school.click()
    
    def _select_school(self, school_name: str):
        self.page.locator(f'div.autocomplete-item[data-value="{school_name}"]').click()

    def _click_submit_button_riad(self):
        self.submit_button_riad.click()

    def _verify_login_success_riad(self):
        expect(self.page.locator("#riaditel-home-page")).to_contain_text("Správa prihlášok")

    def _wait_for_login_success(self):
        expect(self.page).to_have_url(re.compile(".*prihlask.*", re.IGNORECASE))

    def login_as_zakonny_zastupca(self, username: str, password: str):
        self._open_login_form()
        self._fill_username(username)
        self._fill_password(password)
        self._click_login_button()
        self._wait_for_login_success()

    def login_as_riaditel(self, username: str, password: str, school_name: str):
        self._open_login_form_riad()
        self._fill_username(username)
        self._fill_password(password)
        self._click_login_button()
        self._click_on_school()
        self._select_school(school_name)
        self._click_submit_button_riad()
        self._verify_login_success_riad()