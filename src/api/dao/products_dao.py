import random
from utilities.api.db_utility import DbUtility


class ProductsDAO:
    def __init__(self):
        self.db_helper = DbUtility()

    def get_random_product_from_db(self, qty=1):
        sql = f'SELECT * FROM {self.db_helper.database}.wp_posts WHERE post_type = "product" LIMIT 5000;'

        rs_sql = self.db_helper.execute_select(sql)

        return random.sample(rs_sql, int(qty))

    def get_product_by_id(self, product_id):
        sql = f"SELECT * FROM {self.db_helper.database}.wp_posts WHERE ID = {product_id};"
        return self.db_helper.execute_select(sql)

    def get_products_created_after_given_date(self, date):
        sql = f'SELECT * FROM {self.db_helper.database}.wp_posts WHERE post_type = "product" AND post_date >"{date}" LIMIT 10000;'
        return self.db_helper.execute_select(sql)
