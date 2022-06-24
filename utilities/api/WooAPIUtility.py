from src.api.configs.hosts_config import WOO_API_HOSTS
from utilities.api.CredentialsUtility import CredentialUtility
from woocommerce import API
from utilities.common.CustomLogger import CustomLogger
from http import HTTPStatus

import os


class WooAPIUtility(object):

    def __init__(self):
        wc_creds = CredentialUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = WOO_API_HOSTS[self.env]

        self.wcapi = API(
            url=self.base_url,
            consumer_key=wc_creds['wc_key'],
            consumer_secret=wc_creds['wc_secret'],
            version="wc/v3",
            timeout=20,
        )

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code, f"Bad Status code" \
                                                              f"Expected {self.expected_status_code}, Actual status " \
                                                              f"code: {self.status_code}," \
                                                              f"URL: {self.url}, Response Json: {self.rs_json}"

    def post(self, wc_endpoint, params=None, expected_status_code=HTTPStatus.CREATED):
        rs_api = self.wcapi.post(wc_endpoint, data=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.assert_status_code()

        CustomLogger.log().debug(f"API POST response: {self.rs_json}")

        return self.rs_json

    def get(self, wc_endpoint, params=None, expected_status_code=200):
        rs_api = self.wcapi.get(wc_endpoint, params=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.assert_status_code()

        CustomLogger.log().debug(f"API GET response: {self.rs_json}")
        return self.rs_json

    def put(self, wc_endpoint, params=None, expected_status_code=200):
        rs_api = self.wcapi.put(wc_endpoint, data=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.assert_status_code()

        CustomLogger.log().debug(f"API GET response: {self.rs_json}")
        return self.rs_json
