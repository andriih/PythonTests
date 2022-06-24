import allure
import pytest
from utilities.api.RequestsUtility import RequestsUtility


class TestGetAllCustomer:

    @pytest.mark.customers
    @pytest.mark.tcid30
    @pytest.mark.api
    @allure.feature('Customer')
    @allure.title('Retrieve customers list')
    def test_get_all_customers(self):
        req_helper = RequestsUtility()

        with allure.step('Send a request to retrieve a list of customers'):
            rs_api = req_helper.get('customers')

        with allure.step('Ensure that list of customers is returned'):
            assert rs_api, f"Response of list all customers is empty"
