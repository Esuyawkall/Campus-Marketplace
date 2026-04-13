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
            u.user_id,
            i.image_url,
            CASE 
                WHEN f.user_id IS NOT NULL THEN 1
                ELSE 0
            END AS is_favorite
        FROM products p
        JOIN users u ON p.seller_id = u.user_id
        LEFT JOIN favorites f 
            ON p.product_id = f.product_id AND f.user_id = %s
        LEFT JOIN images i ON p.product_id = i.product_id
        """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()
    def getbyProductId(self, product_id):
        sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.product_price,
            p.product_condition,
            u.first_name,
            u.user_id AS seller_id,
            i.image_url
        FROM products p
        JOIN users u ON p.seller_id = u.user_id
        LEFT JOIN images i ON p.product_id = i.product_id
        WHERE p.product_id = %s
        """ 
        self.cur.execute(sql, (product_id,))
        return self.cur.fetchone()
    def CreateListing(self, data):
        try:
            # 1. Insert product first
            sql = """
            INSERT INTO products 
            (product_name, description, product_price, seller_id, product_condition, product_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cur.execute(sql, (
                data['product_name'],
                data['description'],
                data['product_price'],
                data['seller_id'],
                data['product_condition'],
                data['product_status']
            ))

            product_id = self.cur.lastrowid

            image_sql = """
            INSERT INTO images (product_id, image_url)
            VALUES (%s, %s)
            """

            self.cur.execute(image_sql, (
                product_id,
                data['image_url']
            ))

            self.conn.commit()

            return product_id

        except Exception as e:
            self.conn.rollback()
            print("Error:", e)
            return None
    def deleteById(self, id):
        sql = """
        DELETE FROM products
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (id,))
        self.conn.commit()
    def updateProduct(self, id, data):
        sql1 = """
        UPDATE products
        SET product_name = %s,
            description = %s,
            product_price = %s,
            product_condition = %s,
            product_status = %s
        WHERE product_id = %s
        """

        self.cur.execute(sql1, (
            data['product_name'],
            data['description'],
            data['product_price'],
            data['product_condition'],
            data['product_status'],
            id
        ))

        sql2 = """
        UPDATE images
        SET image_url = %s
        WHERE product_id = %s
        """

        self.cur.execute(sql2, (
            data['image_url'],
            id
        ))

        self.conn.commit()
    def getbySellerId(self, seller_id):
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
        WHERE p.seller_id = %s
        """
        self.cur.execute(sql, (seller_id, seller_id))
        return self.cur.fetchall()
