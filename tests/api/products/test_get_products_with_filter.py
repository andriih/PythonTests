import allure
import pytest
from datetime import datetime, timedelta
from src.api.clients.products_client import ProductsClient
from src.api.dao.products_dao import ProductsDAO
from utilities.common.custom_logger import CustomLogger


@allure.title('Test update order customer note')
@pytest.mark.regression
class TestListProductsWithFilter:

    @pytest.mark.api
    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):
        CustomLogger.log().info("create data")
        with allure.step('Generate data:'):
            x_days_from_today = 3000
            _after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
            after_created_date = _after_created_date.isoformat()

        CustomLogger.log().info("make the call")
        with allure.step('Make API call'):
            payload = dict()
            payload['after'] = after_created_date
            rs_api = ProductsClient().call_list_products(payload)

        with allure.step('Verify that response returned'):
            assert rs_api, f"empty response for 'list products with filter"

        CustomLogger.log().info("get data from DB")
        with allure.step('Get data from DB'):
            db_products = ProductsDAO().get_products_created_after_given_date(after_created_date)

        CustomLogger.log().info("verify response")
        with allure.step('Verify API response'):
            assert len(rs_api) == len(
                db_products), f"List products with filter 'After' returned unexpected number of products." \
                              f"Expected: {len(db_products)}, Actual: {len(rs_api)}"

        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_products]

        ids_diff = list(set(ids_in_api) - set(ids_in_db))

        with allure.step('Verify that IDs in API response and DB are equal'):
            assert not ids_diff, f"List products with filter. Product ids in response mismatch in db."
