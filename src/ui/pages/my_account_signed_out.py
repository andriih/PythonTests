
from src.ui.pages.locators import my_account_signed_out_locator
from utilities.common.selenium_extended import SeleniumExtended
from utilities.ui.config_utility import get_base_url
from utilities.common.custom_logger import CustomLogger


class MyAccountSignedOut(my_account_signed_out_locator.MyAccountSignedOutLocator):

    endpoint = '/my-account/'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_my_account(self):
        base_url = get_base_url()
        my_account_url = base_url + self.endpoint
        CustomLogger.log().info(f"Going to: {my_account_url}")

        self.driver.get(my_account_url)

    def input_login_username(self, username):
        self.sl.wait_and_input_text(self.LOGIN_USER_NAME, username)

    def input_login_password(self, password):
        self.sl.wait_and_input_text(self.LOGIN_PASSWORD, password)

    def click_login_button(self):
        CustomLogger.log().debug("Clicking 'login' button.")
        self.sl.wait_and_click(self.LOGIN_BTN)

    def wait_until_error_is_displayed(self):
        self.sl.wait_until_element_is_visible(self. ERRORS_MSG)
        return True

    def input_register_email(self, email):
        self.sl.wait_and_input_text(self.REGISTER_EMAIL, email)

    def input_register_password(self, password):
        self.sl.wait_and_input_text(self.REGISTER_PASSWORD, password)

    def click_register_button(self):
        CustomLogger.log().debug("Clicking 'Register' button.")
        self.sl.wait_and_click(self.REGISTER_BTN)
