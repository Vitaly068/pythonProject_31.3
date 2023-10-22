import pytest
from pages.auth_page import AuthPage

def test_authorisation(web_browser):

    page = AuthPage(web_browser)

    page.email.send_keys('totena@fexbox.org')

    page.password.send_keys("totena")

    page.btn.click()

    assert page.get_current_url() == 'https://petfriends.skillfactory.ru/all_pets'

    #python -m pytest -v --driver Chrome --driver-path C:/Users/Виталий/PycharmProjects/Driver/chromedriver.exe tests/test_auth_page.py
