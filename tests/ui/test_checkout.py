import allure
import pytest
from src.ui.pages.home_page import HomePage
from src.ui.pages.header import Header
from src.ui.pages.cart_page import CartPage
from src.ui.pages.checkout_page import CheckoutPage
from src.ui.pages.order_received_page import OrderReceivedPage
from src.ui.configs.generic_configs import GenericConfigs
from utilities.ui.database_utility import get_order_from_db_by_order_no


@pytest.mark.usefixtures('init_driver')
class TestEndToEndCheckoutGuestUser:

    @pytest.mark.ui
    @pytest.mark.tcid33
    @allure.title('End to End test to check checkout')
    def test_checkout(self):
        with allure.step('Set up'):
            home_p = HomePage(self.driver)
            header = Header(self.driver)
            cart_p = CartPage(self.driver)
            checkout_p = CheckoutPage(self.driver)
            order_received_p = OrderReceivedPage(self.driver)

        with allure.step('Get all product names'):
            home_p.go_to_home_page()
            home_p.click_first_add_to_cart_button()
            header.wait_until_cart_item_count(1)
            header.click_on_cart_on_right_header()
            product_names = cart_p.get_all_product_names_in_cart()

        with allure.step('Verify that one entry returned'):
            assert len(product_names) == 1, f"Expected 1 item in cart but found {len(product_names)}"

        # apply free coupon
        with allure.step('Apply coupon'):
            coupon_code = GenericConfigs.FREE_COUPON
            msg = cart_p.apply_coupon(coupon_code)

        with allure.step('Verify that one entry returned'):
            assert msg == 'Coupon code applied successfully.', f"Unexpected message when applying coupon."

            cart_p.click_on_proceed_to_checkout()
            checkout_p.fill_in_billing_info()
            checkout_p.click_place_order()
            order_received_p.verify_order_received_page_loaded()
            order_no = order_received_p.get_order_number()

        # Check in DB
        with allure.step('Verify  that order created in db'):
            db_order = get_order_from_db_by_order_no(order_no)
            assert db_order, f"Order not found in DB." \
                             f"Order no: {order_no}"
