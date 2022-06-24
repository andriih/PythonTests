

import os

def get_base_url():

    env = os.environ.get('ENV', 'test')

    if env.lower() == 'test':
        return 'http://localhost/wordpress/'
    else:
        raise Exception(f"Unknown environment: {env}")

def get_database_credentials():

    env = os.environ.get('ENV', 'test')

    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    if not db_user or not db_password:
        raise Exception("Environment variables 'DB_USER' and 'DB_PASSWORD' must be set.")

    if env == 'test':
        db_host = 'localhost'
        db_port = 3306
    else:
        raise Exception(f"Unknown environment: {env}")

    db_info = {"db_host": db_host, "db_port": db_port,
               "db_user": db_user, "db_password": db_password}

    return db_info