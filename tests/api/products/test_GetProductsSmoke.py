import allure
import pytest
from utilities.common.CustomLogger import CustomLogger
from utilities.api.RequestsUtility import RequestsUtility
from src.api.dao.ProductsDao import ProductsDAO
from src.api.clients.ProductsClient import ProductsClient


@pytest.mark.products
@pytest.mark.tcid24
@allure.title('Test get all product')
class TestGetProducts:
    def test_get_all_products(self):
        CustomLogger.log().info("Test: Get all products")

        with allure.step('Generate API call'):
            requests_utility = RequestsUtility()
            all_products = requests_utility.get(endpoint='products')

        with allure.step('Generate API call'):
            assert all_products, f"Products are not returned."

    @pytest.mark.products
    @pytest.mark.tcid25
    @allure.title('Test get products by id')
    def test_get_product_by_id(self):
        CustomLogger.log().info("get a product (test data) from db")
        with allure.step('Get test data from DB'):
            rand_product = ProductsDAO().get_random_product_from_db(1)
            rand_product_id = rand_product[0]['ID']
            db_name = rand_product[0]['post_title']

        CustomLogger.log().info("make the call")
        with allure.step('Generate API call'):
            product_helper = ProductsClient()
            rs_api = product_helper.get_product_by_id(rand_product_id)
            api_name = rs_api['name']

        CustomLogger.log().info("verify the response")
        with allure.step('Verify Response'):
            assert db_name == api_name, f"Get product by id returned wrong product. Id: {rand_product_id}" \
                                        f"Db name: {db_name}, Api name: {api_name}"
