import allure
import pytest
from utilities.api.GenericUtilities import generate_random_string
from src.api.clients.ProductsClient import ProductsClient
from src.api.dao.ProductsDao import ProductsDAO


@allure.title('Verify ability to create a product')
class TestProducts:

    @pytest.mark.api
    @pytest.mark.products
    @pytest.mark.tcid26
    def test_create_1_simple_product(self):
        # generate some data
        with allure.step('Generate random data for test'):
            payload = dict()
            payload['name'] = generate_random_string(20)
            payload['type'] = "simple"
            payload['regulal_price'] = "10.99"

        # make the call
        with allure.step('Generate API call'):
            products_rs = ProductsClient().call_create_product(payload)

        # verify the response is not empty
        with allure.step('Verify API response'):
            assert products_rs, f"Create product api response is empty. Payload: {payload}"

        with allure.step('Verify response name'):
            assert products_rs['name'] == payload['name'], f"Create product api call response has" \
                                                           f"unexpected name. Expected: {payload['name']}, Actual: {products_rs['name']}"

        # verify the product exists in
        with allure.step('Verify product exists in DB'):
            product_id = products_rs['id']
            db_product = ProductsDAO().get_product_by_id(product_id)

        with allure.step('Verify product title'):
            assert payload['name'] == db_product[0]['post_title'], f"Create product, title in db does not match " \
                                                                   f"title in api. DB: {db_product['post_title']}, API: {payload['name']}"
