import allure
import pytest
from utilities.common.custom_logger import CustomLogger
from src.ui.pages.my_account_signed_out import MyAccountSignedOut


@pytest.mark.usefixtures("init_driver")
class TestLoginNegative:

    @pytest.mark.tcid12
    @pytest.mark.ui
    @allure.title('End to End test to check checkout')
    def test_login_none_existing_user(self):
        CustomLogger.log().info("TEST LOGIN NON EXISTING")

        fake_name = 'fake_name'

        with allure.step('Login with wrong credentials'):
            my_account = MyAccountSignedOut(self.driver)
            my_account.go_to_my_account()
            my_account.input_login_username(fake_name)
            my_account.input_login_password('124234')
            my_account.click_login_button()
            # import pdb; pdb.set_trace()

        with allure.step('Validate error warning'):
            assert my_account.wait_until_error_is_displayed(), f"Unexpected behavior when login as unknown User"
