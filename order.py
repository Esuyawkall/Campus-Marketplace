from baseObject import baseObject
class order(baseObject):
    def __init__(self):
        self.setup()

    def place_order(self, user_id, product_id, quantity):
        sql = """
        INSERT INTO orders (buyer_id, product_id, quantity, order_status, date_completed)
        VALUES (%s, %s, %s, %s, NOW())
        """ 
        self.cur.execute(sql, (user_id, product_id, quantity, 'Completed'))
        self.conn.commit()
    def get_orders(self, user_id):
        sql = """
        SELECT 
            o.order_id,
            p.product_name,
            p.description,
            p.product_price,
            u.first_name,
            i.image_url,
            p.product_id,
            o.quantity,
            o.order_status,
            o.date_completed
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN users u ON p.seller_id = u.user_id
        LEFT JOIN images i ON p.product_id = i.product_id
        WHERE o.buyer_id = %s
        """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()