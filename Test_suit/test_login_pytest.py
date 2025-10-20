import pytest
from playwright.sync_api import sync_playwright, expect
#---------------
# Test data
#---------------
VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"

INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass"

LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"
SUCCESS_URL = "https://practicetestautomation.com/logged-in-successfully/"

#-----------
# Helper Function
#-----------
def login(page, username, password):
    page.goto(LOGIN_URL)
    page.locator('input#username').fill(username)
    page.locator('input#password').fill(password)
    page.locator('button#submit').click()

#------------
#fixture
#--------------
@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()

#------------
#tests
#------------
def test_valid_login(browser_page):
    login(browser_page,VALID_USERNAME,VALID_PASSWORD)
    browser_page.wait_for_url(SUCCESS_URL)
    expect(browser_page.locator('h1')).to_have_text("Logged In Successfully")
    print(" \nlogin successful")

def test_invalid_username(browser_page):
    login(browser_page,INVALID_USERNAME,VALID_PASSWORD)
    expect(browser_page.locator('div.show')).to_have_text("Your username is invalid!")
    print(" invalid Username")

def test_invalid_password(browser_page):
    login(browser_page,VALID_USERNAME, INVALID_PASSWORD)
    expect(browser_page.locator('div.show')).to_have_text("Your password is invalid!")
    print(" invalid passsword")

def test_empty_cred(browser_page):
    login(browser_page,"","")
    expect(browser_page.locator('div.show')).to_have_text("Your username is invalid!")
    print(" Empty credentials")

