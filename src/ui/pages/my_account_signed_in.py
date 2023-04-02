from src.ui.pages.locators.my_account_signed_in_locators import MyAccountSignedInLocators
from utilities.common.selenium_extended import SeleniumExtended


class MyAccountSignedIn(MyAccountSignedInLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def verify_user_is_signed_in(self):
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)
        return False
