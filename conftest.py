# This is example shows how we can manage failed tests
# and make screenshots after any failed test case.
# Этот пример показывает, как мы можем управлять неудачными тестами
# и делайте скриншоты после любого неудачного теста.

import pytest
import allure
import uuid



@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:
    # Эта функция помогает обнаружить, что какой-то тест не удался
    # # и передайте эту информацию, чтобы снести:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    # Вернуть экземпляр браузера в тестовый пример:
    yield browser

    # Do teardown (this code will be executed after each test):
    # Do teardown (этот код будет выполняться после каждого теста):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        # Сделайте снимок экрана, если тест не удался:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            # Сделайте скриншот для локальной отладки:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # Attach screenshot to Allure report:
            # Прикрепите скриншот к отчету Allure:
            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

            # For happy debugging:
            # Для счастливой отладки:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here # просто игнорируйте любые ошибки здесь


def get_test_case_docstring(item):
    """ This function gets doc string from test case and format it
        to show this docstring instead of the test case name in reports.
    """
    #Эта функция получает строку doc из тестового примера и форматирует ее так, чтобы эта строка
    #документа отображалась вместо имени тестового примера в отчетах

    full_name = ''

    if item._obj.__doc__:
        # Remove extra whitespaces from the doc string:
        # # Удалите лишние пробелы из строки документа:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        # # Сгенерировать список параметров для параметризованных тестовых примеров:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            res_keys = sorted([k for k in params])
            # Create List based on Dict:
            # Создать список на основе Dict:
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Add dict with all parameters to the name of test case:
            # Добавьте dict со всеми параметрами к названию тестового примера:
            full_name += ' Parameters ' + str(', '.join(res))
            full_name = full_name.replace(':', '')

    return full_name


def pytest_itemcollected(item):
    """ This function modifies names of test cases "on the fly"
        during the execution of test cases.
    """
    #Эта функция изменяет имена тестовых примеров "на лету" во время выполнения тестовых примеров

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    """ This function modified names of test cases "on the fly"
        when we are using --collect-only parameter for pytest
        (to get the full list of all existing test cases).
    """
    #Эта функция изменяла названия тестовых примеров "на лету" когда мы используем параметр - -collect - only
    #для pytest (чтобы получить полный список всех существующих тестовых примеров).

    if session.config.option.collectonly is True:
        for item in session.items:
            # If test case has a doc string we need to modify it's name to
            # it's doc string to show human-readable reports and to
            # automatically import test cases to test management system.
            # Если в тестовом примере есть строка документации, нам нужно изменить ее название на
            # это строка документации для отображения удобочитаемых отчетов и для
            # автоматический импорт тестовых наборов в систему управления тестированием.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)

        pytest.exit('Done!')