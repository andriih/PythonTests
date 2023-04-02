import allure
from src.api.dao.orders_dao import OrdersDao
from src.api.clients.customers_client import CustomerClient
import pytest
from utilities.common.custom_logger import CustomLogger


@pytest.mark.usefixtures('my_orders_smoke_setup')
class TestOrders:

    @pytest.mark.api
    @pytest.mark.orders
    @pytest.mark.tcid48
    @allure.feature('Orders')
    @allure.title('Verify that user is able to create paid order')
    def test_create_paid_order_requests_user(self, my_orders_smoke_setup):
        order_helper = my_orders_smoke_setup['order_helper']
        customer_id = 0
        product_id = my_orders_smoke_setup['product_id']
        orders_dao = OrdersDao()

        CustomLogger.log().info("Make the call")

        info = {"line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ]}
        with allure.step('Create an order'):
            order_json = order_helper.create_order(additional_args=info)

        CustomLogger.log().info("verify response")
        expected_products = [{'product_id': product_id}]

        with allure.step('Verify order response'):
            assert order_json, f"Create order response is empty."

        with allure.step('Verify customer id'):
            assert order_json['customer_id'] == customer_id, f"Create order with given customer id " \
                                                             f"Bad customer id. Expected id: {customer_id}, but got {order_json['customer_id']}"

        with allure.step('Verify verify that only one order returned'):
            assert len(order_json['line_items']) == 1, f"Expected only 1 item in order but " \
                                                       f"found '{len(order_json['line_items'])}'" \
                                                       f"Order id: {order_json['id']}"
        with allure.step('verify db'):
            order_id = order_json['id']
            line_info = orders_dao.get_order_lines_by_order_id(order_id)

        with allure.step('Ensure order found in DB'):
            assert line_info, f"Create Order line item not found in DB. Order id: {order_id}"

        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
        with allure.step('Ensure only one order created'):
            assert len(line_items) == 1, f"Expected 1 line item but found {len(line_items)}. Order id: {order_id}"

        with allure.step('get list of product ids in the response'):
            api_product_ids = [i['product_id'] for i in order_json['line_items']]

        for product in expected_products:
            with allure.step(f"Ensure product id: {product['product_id']} present in order "):
                assert product[
                           'product_id'] in api_product_ids, f"Created order does not have at least 1 expected product in DB" \
                                                             f"Product id: {product['product_id']}. Order id: {order_id}"

    @pytest.mark.api
    @pytest.mark.orders
    @pytest.mark.tcid49
    @allure.feature('Orders')
    @allure.title('Verify that NEW user is able to create paid order')
    def test_create_order_paid_order_new_created_customer(self, my_orders_smoke_setup):
        CustomLogger.log().info("create helper objects")
        order_helper = my_orders_smoke_setup['order_helper']
        customer_helper = CustomerClient()
        orders_dao = OrdersDao()

        CustomLogger.log().info("make the call")
        cust_info = customer_helper.create_customer()
        customer_id = cust_info['id']
        product_id = my_orders_smoke_setup['product_id']

        info = {"line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ],
            "customer_id": customer_id}

        with allure.step('Create an order'):
            order_json = order_helper.create_order(additional_args=info)

        expected_products = [{'product_id': product_id}]

        with allure.step('Verify order response'):
            assert order_json, f"Create order response is empty."

        with allure.step('Verify customer id'):
            assert order_json['customer_id'] == customer_id, f"Create order with given customer id " \
                                                             f"Bad customer id. Expected id: {customer_id}, but got {order_json['customer_id']}"

        with allure.step('Verify verify that only one order returned'):
            assert len(order_json['line_items']) == 1, f"Expected only 1 item in order but " \
                                                       f"found '{len(order_json['line_items'])}'" \
                                                       f"Order id: {order_json['id']}"
        CustomLogger.log().info("verify db")
        order_id = order_json['id']
        line_info = orders_dao.get_order_lines_by_order_id(order_id)
        with allure.step('Ensure order found in DB'):
            assert line_info, f"Create Order line item not found in DB. Order id: {order_id}"

        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
        with allure.step('Ensure only one order created'):
            assert len(line_items) == 1, f"Expected 1 line item but found {len(line_items)}. Order id: {order_id}"

        CustomLogger.log().info("get list of product ids in the response")
        api_product_ids = [i['product_id'] for i in order_json['line_items']]

        for product in expected_products:
            with allure.step(f"Ensure product id: {product['product_id']} present in order "):
                assert product[
                           'product_id'] in api_product_ids, f"Created order does not have at least 1 expected product in DB" \
                                                             f"Product id: {product['product_id']}. Order id: {order_id}"
