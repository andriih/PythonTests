from utilities.api.db_utility import DbUtility


class OrdersDao:
    def __init__(self):
        self.db_helper = DbUtility()

    def get_order_lines_by_order_id(self, order_id):
        sql = f'SELECT * FROM {self.db_helper.database}.wp_woocommerce_order_items WHERE order_id = {order_id};'
        return self.db_helper.execute_select(sql)

    def get_order_items_line_details(self, order_item_id):
        sql = f"SELECT * FROM {self.self.db_helper.database}.wp_woocommerce_order_itemmeta WHERE order_item_id = {order_item_id};"
        rs_sql = self.db_helper.execute_select(sql)
        line_details = dict()
        for meta in rs_sql:
            line_details[meta['meta_key']] = meta['meta_value']

        return line_details
