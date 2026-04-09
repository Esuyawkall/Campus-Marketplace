from baseObject import baseObject
class order(baseObject):
    def __init__(self):
        self.setup()

    def place_order(self, user_id, product_id, quantity):
        sql = """
        INSERT INTO orders (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        """ 
        self.cur.execute(sql, (user_id, product_id, quantity))
        self.conn.commit()
    def get_orders(self, user_id):
        sql = """
        SELECT o.*, p.product_name, p.product_price, p.seller_id, u.first_name AS seller_name
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN users u ON o.buyer_id = u.user_id
        WHERE o.buyer_id = %s
        """ 
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()