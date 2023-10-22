import pytest
import time
from pages.yandex import MainPage



# def test_check_main_search(web_browser):
#     """ Make sure main search works fine. """
#     #Убедитесь, что основной поиск работает нормально
#
#     page = MainPage(web_browser)
#     time.sleep(20)
#
#     page.search = "iphone 15"
#     page.search_run_button.click()
#
#     # Verify that user can see the list of products:
#     # Проверяем  наличие продуктов на странице:
#     # assert page.products_titles.count() == 48
#     # assert page.products_titles.count() != 48
#     # assert page.products_titles.count() > 0
#
#     # Make sure user found the relevant products
#     # Проверяем наличие в названии слова iphone
#     for title in page.products_titles.get_text():
#         msg = 'Wrong product in search "{}"'.format(title)
#         assert 'iphone' in title.lower(), msg
#
#
# def test_check_wrong_input_in_search(web_browser):
#     """ Make sure that wrong keyboard layout input works fine. """
#     #Убедитесь, что ввод с неправильной раскладкой клавиатуры работает нормально
#
#     page = MainPage(web_browser)
#     time.sleep(20)
#
#     # Try to enter "смартфон" with English keyboard:
#     page.search = "cvfhnajy ltncrbq"
#     page.search_run_button.click()
#
#     # Verify that user can see the list of products:
#     #Убедитесь, что пользователь может видеть список продуктов:
#     # assert page.products_titles.count() == 48
#     # assert page.products_titles.count() != 48
#     # assert page.products_titles.count() > 0
#
#     # Make sure user found the relevant products
#     #Убедитесь, что пользователь нашел соответствующие продукты
#     for title in page.products_titles.get_text():
#         msg = 'Wrong product in search "{}"'.format(title)
#         assert 'смартфон' in title.lower(), msg


# @pytest.mark.xfail(reason="Filter by price doesn't work")
def test_check_sort_by_price(web_browser):
    # Проверка сортировки продуктов
    """ Make sure that sort by price works fine.

        Note: this test case will fail because there is a bug in
              sorting products by price.
    """
    #Убедитесь, что сортировка по цене работает нормально.
    #Примечание: этот тестовый пример завершится неудачей из-за ошибки в
    #сортировке товаров по цене.

    page = MainPage(web_browser)
    time.sleep(20)

    page.search = "чайник 'ktrnhbxtcrbq"
    page.search_run_button.click()

    # Scroll to element before click on it to make sure
    # user will see this element in real browser
    # Выделите элемент, прежде чем щелкнуть по нему, чтобы убедиться
    # пользователь увидит этот элемент в реальном браузере
    page.sort_products_by_price.scroll_to_element()
    page.sort_products_by_price.click()
    page.wait_page_loaded()

    # Get prices of the products in Search results
    # Получить цены на товары в результатах поиска
    all_prices = page.products_prices.get_text()

    # Convert all prices from strings to numbers
    # Преобразовать все цены из строк в числа
    # all_prices = [float(p.replace(' ', '')) for p in all_prices]
    all_prices = [int(float(p.replace('"', ''))) for p in all_prices]

    # print(all_prices)
    # print(sorted(all_prices))

    # Make sure products are sorted by price correctly:
    # Убедитесь, что товары правильно отсортированы по цене:
    assert all_prices == sorted(all_prices), "Sort by price doesn't work!"

    print(float(all_prices))
    # print(sorted(all_prices))




    #запуск теста python -m pytest -v --driver Chrome --driver-path C:/Users/Виталий/PycharmProjects/Driver/chromedriver.exe tests/test_smoke_yandex_market.py