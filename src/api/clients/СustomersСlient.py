from utilities.api.GenericUtilities import generate_random_email_and_password
from utilities.api.RequestsUtility import RequestsUtility


class CustomerClient(object):
    def __init__(self):
        self.requests_utility = RequestsUtility()

    def create_customer(self, email=None, password=None, **kwargs):

        if not email:
            ep = generate_random_email_and_password()
            email = ep['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        create_user_json = self.requests_utility.post('customers', payload=payload)

        return create_user_json
