import random

import allure
import pytest
from src.api.clients.orders_client import OrdersClient
from utilities.api.woo_api_utility import WooAPIUtility
from utilities.api.generic_utilities import generate_random_string

pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.parametrize("new_status", [
    pytest.param('cancelled', marks=pytest.mark.tcid55),
    pytest.param('completed', marks=pytest.mark.tcid56),
    pytest.param('on-hold', marks=pytest.mark.tcid57)
])
@allure.title('Test update order status')
@pytest.mark.api
def test_update_order_status(new_status):
    possible_status_list = ['cancelled', 'completed', 'on-hold']
    # create new order
    order_helper = OrdersClient()

    with allure.step('Create an order for parametrized test'):
        order_json = order_helper.create_order()

    cur_status = order_json['status']
    order_id = order_json['id']

    possible_choices = [v for v in possible_status_list if v != cur_status]
    rand_status = random.choice(possible_choices)
    # import pdb; pdb.set_trace()
    payload = {"status": rand_status}
    order_helper.call_update_an_order(order_id, payload)

    with allure.step('Verify that order status is not updated already to expected status'):
        assert cur_status != rand_status, f"Current status of order is already '{rand_status}'. " \
                                          f"Unable to run test."

    # update the status
    # order_id = order_json['id']
    payload = {"status": new_status}
    with allure.step('Call API to update order'):
        order_helper.call_update_an_order(order_id, payload)

    # get order info
    with allure.step('Retrieve updated order'):
        new_order_info = order_helper.call_retrive_an_order(order_id)

    with allure.step('Verify that order status is updated'):
        assert new_order_info['status'] == new_status, f"Updated order status to {new_status}, " \
                                                       f"but order is still '{new_order_info['status']}'"


@pytest.mark.tcid58
@allure.title('Test update order status to random string')
@pytest.mark.api
def test_update_order_status_to_random_string():
    new_status = 'abcdfg'

    # create new order
    order_client = OrdersClient()
    with allure.step('Create an order'):
        order_json = order_client.create_order()
        order_id = order_json['id']

    # update the status
    payload = {"status": new_status}

    with allure.step('Get API response'):
        rs_api = WooAPIUtility().put(f'orders/{order_id}', params=payload, expected_status_code=400)

    with allure.step('Verify API response code'):
        assert rs_api['code'] == 'rest_invalid_param', f"Update order status to random string did not have " \
                                                       "correct code in response. Expected: 'rest_invalid_param' " \
                                                       f"Actual: {rs_api['code']}"

    with allure.step('Verify API response message'):
        assert rs_api[
                   'message'] == 'Invalid parameter(s): status', f"Update order status to random string did not have " \
                                                                 "correct message in response. Expected: 'Invalid " \
                                                                 "parameter(s): status' " \
                                                                 f"Actual: {rs_api['message']}"


@pytest.mark.tcid59
@pytest.mark.api
@allure.title('Test update order customer note')
def test_update_order_customer_note():
    order_client = OrdersClient()

    with allure.step('Create an order'):
        order_json = order_client.create_order()
        order_id = order_json['id']

    rand_string = generate_random_string(40)
    payload = {"customer_note": rand_string}

    with allure.step('Update an order'):
        order_client.call_update_an_order(order_id, payload)

    # get order info
    with allure.step('Get updated order'):
        new_order_info = order_client.call_retrive_an_order(order_id)

    with allure.step('Verify that customer notes got updated'):
        assert new_order_info['customer_note'] == str(rand_string), f"Update orders 'customer_note' field failed." \
                                                                    f"Expected: {rand_string}, Actual: {new_order_info['customer_note']}"
