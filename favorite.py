from baseObject import baseObject
class favorite(baseObject):
    def __init__(self):
        self.setup()

    def toggle_favorite(self, user_id, product_id):
        sql = """
        SELECT *
        FROM favorites
        WHERE user_id = %s AND product_id = %s
        """ 
        self.cur.execute(sql, (user_id, product_id))
        result = self.cur.fetchone()

        if result:
            sql = """
            DELETE FROM favorites
            WHERE user_id = %s AND product_id = %s
            """ 
            self.cur.execute(sql, (user_id, product_id))
        else:
            sql = """
            INSERT INTO favorites (user_id, product_id)
            VALUES (%s, %s)
            """ 
            self.cur.execute(sql, (user_id, product_id))
        
        self.conn.commit()
    def get_favorites(self, user_id):
        sql = """
        SELECT products.*, favorites.user_id AS is_favorite
        FROM products
        LEFT JOIN favorites ON products.product_id = favorites.product_id AND favorites.user_id = %s
        """ 
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchall()