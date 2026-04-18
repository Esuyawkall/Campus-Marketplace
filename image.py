from baseObject import baseObject
class image(baseObject):
    def __init__(self):
        self.setup()

    def add_image(self, product_id, image_url):
        sql = """
        INSERT INTO images (product_id, image_url)
        VALUES (%s, %s)
        """ 
        self.cur.execute(sql, (product_id, image_url))
        self.conn.commit()
    def get_images_by_product_id(self, product_id):
        sql = """
        SELECT image_url, image_id
        FROM images
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (product_id,))
        results = self.cur.fetchall()
        return [
            {"image_id": row["image_id"], "url": row["image_url"]}
            for row in results
                ]
    def delete_images_by_product_id(self, product_id):
        sql = """
        DELETE FROM images
        WHERE product_id = %s
        """ 
        self.cur.execute(sql, (product_id,))
        self.conn.commit()
    def update_image(self, image_id, new_url):
        sql = """
        UPDATE images
        SET image_url = %s
        WHERE image_id = %s
        """ 
        self.cur.execute(sql, (new_url, image_id))
        self.conn.commit()
    def get_valid_image(self, images):
        if images:
            for img in images:
                url = img.get('url')

                if url and isinstance(url, str) and url.strip():
                    return url
        else:
            return '/static/images/desk+chair.jpg'
        return '/static/images/desk+chair.jpg'