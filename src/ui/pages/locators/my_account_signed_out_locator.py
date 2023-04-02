from selenium.webdriver.common.by import By


class MyAccountSignedOutLocator:
    LOGIN_USER_NAME = (By.ID, 'username')
    LOGIN_PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button[value="Log in"]')

    ERRORS_UL = (By.CSS_SELECTOR, '#content > div > div.woocommerce > ul > li > strong:nth-child(2)')
    ERRORS_MSG = (By.XPATH, "//*[contains(text(),'Error')]")

    REGISTER_EMAIL = (By.ID, 'reg_email')
    REGISTER_PASSWORD = (By.ID, 'reg_password')
    REGISTER_BTN = (By.CSS_SELECTOR, 'button[value="Register"]')
