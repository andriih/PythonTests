import os.path
import json
from utilities.api.woo_api_utility import WooAPIUtility
from utilities.common.custom_logger import CustomLogger


class OrdersClient(object):
    def __init__(self):
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = WooAPIUtility()

    def create_order(self, additional_args=None):
        payload_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_patload.json')

        with open(payload_template) as f:
            payload = json.load(f)

        CustomLogger.log().info("if user adds more info to payload, then update it")
        if additional_args:
            assert isinstance(additional_args,
                              dict), f"Parameter 'additional_args' must be a dictionary but found {type(additional_args)}"
            payload.update(additional_args)

        rs_api = self.woo_helper.post('orders', params=payload, expected_status_code=201)

        return rs_api

    def call_update_an_order(self, order_id, payload):
        return self.woo_helper.put(f'orders/{order_id}', params=payload)

    def call_retrive_an_order(self, order_id):
        return self.woo_helper.get(f"orders/{order_id}")
