from baseObject import baseObject
class favorite(baseObject):
    def __init__(self):
        self.setup()

    def toggle_favorite(self, user_id, product_id):
    # check if already liked
        sql = "SELECT * FROM favorites WHERE user_id=%s AND product_id=%s"
        self.cur.execute(sql, (user_id, product_id))
        existing = self.cur.fetchone()

        if existing:
            # remove like
            sql = "DELETE FROM favorites WHERE user_id=%s AND product_id=%s"
            self.cur.execute(sql, (user_id, product_id))
            self.conn.commit()
            return False
        else:
            # add like
            sql = "INSERT INTO favorites (user_id, product_id) VALUES (%s, %s)"
            self.cur.execute(sql, (user_id, product_id))
            self.conn.commit()
            return True
    def get_favorites(self, user_id):
        sql = """
            SELECT 
                p.*,u.first_name,
                (
            SELECT i.image_url
            FROM images i
            WHERE i.product_id = p.product_id
            LIMIT 1
            ) AS image_url,

            CASE 
                WHEN f.user_id IS NOT NULL THEN 1
                ELSE 0
            END AS is_favorite

            FROM products p
            JOIN users u 
                ON p.seller_id = u.user_id

            LEFT JOIN favorites f 
                ON p.product_id = f.product_id 
                AND f.user_id = %s
                """
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()