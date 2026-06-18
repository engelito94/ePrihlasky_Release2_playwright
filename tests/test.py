import re
import os
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_example(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.login_as_zakonny_zastupca(
        username=os.getenv("EPRIHLASKY_ZZ_USERNAME"),
        password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
    )