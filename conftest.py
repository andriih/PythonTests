import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
import os
import allure
from src.api.dao.products_dao import ProductsDAO
from src.api.clients.orders_client import OrdersClient
from utilities.common.custom_logger import CustomLogger


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to notify before and after a test is run"""
    # Setup:
    CustomLogger.log().info(f"======== START TEST: {os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]}")
    yield
    # Teardown
    CustomLogger.log().info(f"======== END TEST: {os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]}")


@pytest.fixture
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    order_helper = OrdersClient()
    info = {'product_id': product_id, 'order_helper': order_helper}
    return info


@pytest.fixture
def init_driver(request):
    pass
    supported_browsers = ["chrome", "ch", "headlesschrome"]

    browser = os.environ.get('BROWSER', None)
    if not browser:
        raise Exception("The environment variable 'Browser' must be set.")

    browser = browser.lower()
    if browser not in supported_browsers:
        raise Exception(f"Provide browser '{browser}' is not one of the supported."
                        f"Supported are: {supported_browsers}")

    if browser in ('chrome', 'ch'):
        driver = webdriver.Chrome()
    elif browser in ('headlesschrome'):
        chrome_options = ChOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

    request.cls.driver = driver
    yield
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            is_frontend_test = True if 'init_driver' in item.fixturenames else False
            if is_frontend_test:
                results_dir = os.environ.get("RESULTS_DIR")
                if not results_dir:
                    raise Exception("Environment variable 'RESULTS_DIR' must be set.")
                driver_fixture = item.funcargs['request']
                allure.attach(driver_fixture.cls.driver.get_screenshot_as_png(),
                              name='screenshot',
                              attachment_type=allure.attachment_type.PNG)
