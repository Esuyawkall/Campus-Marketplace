from baseObject import baseObject
class order(baseObject):
    def __init__(self):
        self.setup()

    def place_order(self, user_id, product_id, quantity):
        try:
            # First, get the seller_id from the product
            sql_seller = "SELECT seller_id FROM products WHERE product_id = %s"
            self.cur.execute(sql_seller, (product_id,))
            result = self.cur.fetchone()
            
            if not result:
                return {"error": "Product not found."}
            
            seller_id = result['seller_id']
            
            # Now insert the order with seller_id
            sql = """
            INSERT INTO orders (buyer_id, product_id, quantity, seller_id, order_status, date_completed)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """ 
            self.cur.execute(sql, (user_id, product_id, quantity, seller_id, 'Completed'))
            self.conn.commit()

            return {"success": "Order placed successfully."}

        except Exception as e:
            if "Duplicate entry" in str(e):
                return {"error": "You have already ordered this item."}
            raise e
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
    def get_order_summary_by_user_id(self, user_id):
        sql = """
        SELECT SUM(p.product_price*o.quantity) AS total_realized_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'completed' AND o.seller_id = %s;
        """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()
    def get_order_summary_by_product_id(self, product_id):
        sql = """
        SELECT SUM(p.product_price*o.quantity) AS total_realized_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'completed' AND o.product_id = %s;
        """
        self.cur.execute(sql, (product_id,))
        return self.cur.fetchall()
    def get_pending_orders_summary_by_user_id(self, user_id):
        sql = """
        SELECT SUM(p.product_price*o.quantity) AS total_pending_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'pending' AND o.seller_id = %s;
        """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()
    
    def has_user_ordered_product(self, user_id, product_id):
        """Check if a user has already ordered a specific product"""
        sql = """
        SELECT COUNT(*) as count
        FROM orders
        WHERE buyer_id = %s AND product_id = %s
        """
        self.cur.execute(sql, (user_id, product_id))
        result = self.cur.fetchone()
        return result['count'] > 0 if result else False

    def get_user_order_stats(self, user_id):
        sql = """
        SELECT
            COUNT(CASE WHEN o.buyer_id = %s THEN 1 END) AS buyer_total_orders,
            COUNT(CASE WHEN o.buyer_id = %s AND LOWER(o.order_status) = 'completed' THEN 1 END) AS buyer_completed_orders,
            COUNT(CASE WHEN o.buyer_id = %s AND LOWER(o.order_status) = 'pending' THEN 1 END) AS buyer_pending_orders,
            COUNT(CASE WHEN o.buyer_id = %s AND LOWER(o.order_status) NOT IN ('completed', 'pending') THEN 1 END) AS buyer_other_orders,
            ROUND(COALESCE(SUM(CASE WHEN o.buyer_id = %s THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS buyer_total_spend,
            ROUND(COALESCE(SUM(CASE WHEN o.buyer_id = %s AND LOWER(o.order_status) = 'completed' THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS buyer_completed_spend,
            ROUND(COALESCE(SUM(CASE WHEN o.buyer_id = %s AND LOWER(o.order_status) = 'pending' THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS buyer_pending_spend,
            COUNT(CASE WHEN p.seller_id = %s THEN 1 END) AS seller_total_sales,
            COUNT(CASE WHEN p.seller_id = %s AND LOWER(o.order_status) = 'completed' THEN 1 END) AS seller_completed_sales,
            COUNT(CASE WHEN p.seller_id = %s AND LOWER(o.order_status) = 'pending' THEN 1 END) AS seller_pending_sales,
            COUNT(CASE WHEN p.seller_id = %s AND LOWER(o.order_status) NOT IN ('completed', 'pending') THEN 1 END) AS seller_other_sales,
            ROUND(COALESCE(SUM(CASE WHEN p.seller_id = %s THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS seller_total_sales_value,
            ROUND(COALESCE(SUM(CASE WHEN p.seller_id = %s AND LOWER(o.order_status) = 'completed' THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS seller_completed_revenue,
            ROUND(COALESCE(SUM(CASE WHEN p.seller_id = %s AND LOWER(o.order_status) = 'pending' THEN p.product_price * o.quantity ELSE 0 END), 0), 2) AS seller_pending_revenue,
            ROUND(COALESCE(AVG(CASE WHEN p.seller_id = %s THEN p.product_price * o.quantity END), 0), 2) AS seller_avg_sale_value,
            ROUND(COALESCE(MAX(CASE WHEN p.seller_id = %s THEN p.product_price * o.quantity END), 0), 2) AS seller_largest_sale
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.buyer_id = %s OR p.seller_id = %s
        """
        params = (
            user_id, user_id,
            user_id, user_id, user_id, user_id, user_id,
            user_id, user_id, user_id, user_id,
            user_id, user_id, user_id, user_id, user_id,
            user_id, user_id
        )
        self.cur.execute(sql, params)
        return self.cur.fetchone()