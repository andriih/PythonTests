import random
import string
from utilities.common.CustomLogger import CustomLogger


def generate_random_email_and_password(domain=None, email_prefix=None):
    CustomLogger.log().info("Generating random email and password")

    if not domain:
        domain = 'andriitest.com'
    if not email_prefix:
        email_prefix = 'testuser'

    random_email_string_lenght = 10
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_lenght))

    email = email_prefix + '_' + str(random_string) + '@' + domain

    password_string = ''.join(random.choices(string.ascii_letters, k=random_email_string_lenght))

    random_info = {'email': email, 'password': password_string}
    CustomLogger.log().debug(f"Randomly generated email and password: {random_info}")

    return random_info


def generate_random_string(length=10, prefix=None, suffix=None):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string + suffix

    return random_string
