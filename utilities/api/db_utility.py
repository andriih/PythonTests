import pymysql
import os
from utilities.api.credentials_utility import CredentialUtility
from src.api.configs.hosts_config import DB_HOST
from utilities.common.custom_logger import CustomLogger


class DbUtility(object):
    def __init__(self):
        creds_helper = CredentialUtility()
        self.creds = creds_helper.get_db_credentials()

        self.machine = os.environ.get('MACHINE')
        assert self.machine, f"Environment variable 'MACHINE' must be set."

        self.wp_host = os.environ.get('WP_HOST')
        assert self.wp_host, f"Environment variable 'WP_HOST' must be set."

        if self.machine == 'docker' and self.wp_host == 'localhost':
            raise Exception(f"Can not run test in docker if WP_HOST=localhost")

        self.env = os.environ.get('ENV', 'test')

        self.host = DB_HOST[self.machine][self.env]['host']
        self.port = DB_HOST[self.machine][self.env]['port']
        self.database = DB_HOST[self.machine][self.env]['database']
        self.table_prefix = DB_HOST[self.machine][self.env]['table_prefix']

    def create_connection(self):
        if self.wp_host == 'localhost':
            connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                         password=self.creds['db_password'],
                                         port=self.port)
        else:
            raise Exception("Unknown WP_HOST.")

        return connection

    def execute_select(self, sql):

        conn = self.create_connection()

        try:
            CustomLogger.log().debug(f"Executing: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict

    def execute_sql(self, sql):
        pass
