import re
import os
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.test_data_file import pop_random_person_from_file
from utils.test_mail import Mail

def test_example(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.login_as_zakonny_zastupca(
        username=os.getenv("EPRIHLASKY_ZZ_USERNAME"),
        password=os.getenv("EPRIHLASKY_ZZ_PASSWORD")
    )

def test_riaditel(page: Page) -> None:
    mail = Mail()   
    a = mail.get_six_digit_number_from_last_email(
        host="imap.gmail.com",
        user=os.getenv("GMAIL_USERNAME"),
        password=os.getenv("GMAIL_APP_PASSWORD")
    ) 
    print(a)



