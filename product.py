from baseObject import baseObject

class product(baseObject):
    def __init__(self):
        self.setup()

    def getAll(self, user_id):
        sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.product_price,
            u.first_name,
            CASE 
                WHEN f.user_id IS NOT NULL THEN 1
                ELSE 0
            END AS is_favorite
        FROM products p
        JOIN users u ON p.seller_id = u.user_id
        LEFT JOIN favorites f 
            ON p.product_id = f.product_id AND f.user_id = %s
        """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()
    def getbyProductId(self, product_id):
        sql = """
        SELECT *
        FROM products
        JOIN users ON products.seller_id = users.user_id
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (product_id,))
        return self.cur.fetchone()
    def CreateListing(self, data):
        sql = """
        INSERT INTO products (product_name, description, product_price, seller_id, product_condition, product_status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """ 
        self.cur.execute(sql, (data['product_name'], data['description'], data['product_price'], data['seller_id'], data['product_condition'], data['product_status']))
        self.conn.commit()
    def deleteById(self, id):
        sql = """
        DELETE FROM products
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (id,))
        self.conn.commit()
    def updateProduct(self, id, data):
        sql = """
        UPDATE products
        SET name = %s, description = %s, price = %s
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (data['name'], data['description'], data['price'], id))
        self.conn.commit()
    
