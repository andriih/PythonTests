from utilities.api.requests_utility import RequestsUtility
from utilities.common.custom_logger import CustomLogger


class ProductsClient(object):
    def __init__(self):
        self.requests_utility = RequestsUtility()

    def get_product_by_id(self, product_id):
        return self.requests_utility.get(f"products/{product_id}")

    def call_create_product(self, payload):
        return self.requests_utility.post('products', payload=payload, expected_status_code=201)

    def call_list_products(self, payload=None):
        max_pages = 1000
        all_products = []
        for i in range(1, max_pages + 1):
            CustomLogger.log().debug(f"List products page number: {i}")

            if 'per_page' in payload.keys():
                payload['per_page'] = 3

            CustomLogger.log().debug("add page number")
            payload['page'] = i
            rs_api = self.requests_utility.get('products', payload=payload)

            CustomLogger.log().debug("stop the loop")
            if not rs_api:
                break
            else:
                all_products.extend(rs_api)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")

        return all_products
