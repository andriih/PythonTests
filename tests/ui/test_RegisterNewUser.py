import allure
import pytest
from utilities.common.CustomLogger import CustomLogger
from src.ui.pages.MyAccountSignedOut import MyAccountSignedOut
from src.ui.pages.MyAccountSignedIn import MyAccountSignedIn
from utilities.ui.GenericUtility import generate_random_email_and_password


@pytest.mark.usefixtures("init_driver")
class TestRegisterNewUser:

    @pytest.mark.ui
    @pytest.mark.tcid13
    def test_register_valid_new_user(self):
        CustomLogger.log().info("TEST REGISTER NEW USER")

        with allure.step('Go to my account page'):
            my_account_o = MyAccountSignedOut(self.driver)
            my_account_i = MyAccountSignedIn(self.driver)
            my_account_o.go_to_my_account()

        with allure.step('Insert valid creds -> click thr Register button'):
            rand_email = generate_random_email_and_password()
            my_account_o.input_register_email(rand_email["email"])
            my_account_o.input_register_password('Wordpress_1_Test_@')
            my_account_o.click_register_button()

        with allure.step('Verify that new user successfully registered'):
            assert my_account_i.verify_user_is_signed_in(), "Cannot register new user"
