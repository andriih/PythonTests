import allure
import pytest
from utilities.common.CustomLogger import CustomLogger
from utilities.api.GenericUtilities import generate_random_email_and_password
from src.api.clients.СustomersСlient import CustomerClient
from src.api.dao.CustomersDao import CustomersDAO
from utilities.api.RequestsUtility import RequestsUtility

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestUserCreation:

    @pytest.mark.tcid29
    @pytest.mark.api
    @allure.feature('Customer')
    @allure.title('Create custom with only email and password')
    def test_create_customer_only_email_password(self):
        CustomLogger.log().info("Test: Create new customer with email and password only.")
        rand_info = generate_random_email_and_password()
        email = rand_info['email']
        password = rand_info['password']

        CustomLogger.log().info('make the call')
        cust_obj = CustomerClient()

        with allure.step('Create new customer'):
            cust_api_info = cust_obj.create_customer(email=email, password=password)

        # verify email and first name in the response
        with allure.step('Verify that customer created with correct Email address'):
            assert cust_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"

        with allure.step('Verify that customer created with correct Login name'):
            assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                                      f"but it should be empty."
        # verify customer is created in database
        with allure.step('Retrieve customer from DB'):
            cust_dao = CustomersDAO()
            cust_info = cust_dao.get_customer_by_email(email)

        id_in_api = cust_api_info['id']
        id_in_db = cust_info[0]['ID']

        with allure.step('Ensure that customer created in DB'):
            assert id_in_api == id_in_db, f'Create customer response "id" not same as "ID" in database,' \
                                          f'Email: {email}'

    @pytest.mark.tcid47
    @allure.feature('Customer')
    @pytest.mark.api
    @allure.title('Create custom with existing email')
    def test_create_customer_fail_for_existing_email(self):
        CustomLogger.log().info('get existing email from db')
        cust_dao = CustomersDAO()

        with allure.step('Get random customer '):
            existing_cust = cust_dao.get_random_customer_from_db()

        existing_email = existing_cust[0]['user_email']

        CustomLogger.log().info('Call the API')
        req_helper = RequestsUtility()
        payload = {"email": existing_email, "password": "Password1"}

        with allure.step('Send request to create new customer'):
            cust_api_info = req_helper.post(endpoint='customers', payload=payload, expected_status_code=400)

        with allure.step('Ensure that error is displayed'):
            assert cust_api_info['code'] == 'registration-error-email-exists', f"Create customer with" \
                                                                               f"Expected 'registration-error-email" \
                                                                               f"Actual: {cust_api_info['code']}"
