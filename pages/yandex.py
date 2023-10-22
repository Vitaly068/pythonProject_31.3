import os

from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or 'https://market.yandex.ru/'

        super().__init__(web_driver, url)

    # поле поиска
    search = WebElement(id='header-search')

    # Search button
    # кнопка поиска
    search_run_button = WebElement(xpath='//button[@type="submit"]')

    # Titles of the products in search results
    # Название продуктов  в списке
    products_titles = ManyWebElements(xpath='//a[contains(@href, "/product-") and @title!=""]')

    # Button to sort products by price
    # Кнопка сортировки по цене
    sort_products_by_price = WebElement(css_selector='button[data-autotest-id="dprice"]')

    # Prices of the products in search results
    # Цены продукта
    products_prices = ManyWebElements(xpath='//div[@data-zone-name="price"]//span/*[1]')