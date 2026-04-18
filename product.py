from baseObject import baseObject


class product(baseObject):
    def __init__(self):
        self.setup()

<<<<<<< HEAD
    # -----------------------------
    # GET ALL PRODUCTS
    # -----------------------------
    def getAll(self, user_id, is_admin=False, search=None):
=======
    def getAll(self, user_id, is_admin=False):
>>>>>>> d889270 (apply gitignore properly)
        sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.product_price,
            p.product_condition,
            p.product_status,
<<<<<<< HEAD
            p.seller_id,
=======
>>>>>>> d889270 (apply gitignore properly)
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
        WHERE (%s = 1 OR p.product_status <> 'unavailable' OR p.seller_id = %s)
        """
<<<<<<< HEAD
        params = [user_id, int(is_admin), user_id]

        if search:
            sql += """
            AND (
                p.product_name LIKE %s
                OR p.description LIKE %s
                OR p.product_condition LIKE %s
            )
            """
            like = f"%{search}%"
            params.extend([like, like, like])

        self.cur.execute(sql, tuple(params))
        rows = self.cur.fetchall()

        return self._attach_image_url(rows)

    # -----------------------------
    # GET BY PRODUCT ID
    # -----------------------------
=======
        self.cur.execute(sql, (user_id, int(is_admin), user_id))
        return self.cur.fetchall()
>>>>>>> d889270 (apply gitignore properly)
    def getbyProductId(self, product_id):
        sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.product_price,
            p.product_condition,
            p.product_status,
<<<<<<< HEAD
            p.seller_id,
=======
>>>>>>> d889270 (apply gitignore properly)
            u.first_name,
            u.user_id AS seller_id,
            i.image_url
        FROM products p
        JOIN users u ON p.seller_id = u.user_id
        LEFT JOIN images i ON p.product_id = i.product_id
        WHERE p.product_id = %s
        """

        self.cur.execute(sql, (product_id,))
        row = self.cur.fetchone()

        if row:
            return self._attach_image_url([row])[0]
        return None

    # -----------------------------
    # CREATE PRODUCT
    # -----------------------------
    def CreateListing(self, data):
        try:
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

            # store ONLY filename (NOT full path)
            image_sql = """
            INSERT INTO images (product_id, image_url)
            VALUES (%s, %s)
            """

            self.cur.execute(image_sql, (
                product_id,
                data['image_url']  # should be filename only
            ))

            self.conn.commit()
            return product_id

        except Exception as e:
            self.conn.rollback()
            print("CreateListing Error:", e)
            return None

    # -----------------------------
    # DELETE PRODUCT
    # -----------------------------
    def deleteById(self, id):
        sql = "DELETE FROM products WHERE product_id = %s"
        self.cur.execute(sql, (id,))
        self.conn.commit()

    # -----------------------------
    # UPDATE PRODUCT
    # -----------------------------
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
            data['image_url'],  # filename only
            id
        ))

        self.conn.commit()

    # -----------------------------
    # GET BY SELLER ID
    # -----------------------------
    def getbySellerId(self, seller_id, search=None):
        sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.product_price,
            p.product_condition,
            p.product_status,
<<<<<<< HEAD
            p.seller_id,
=======
>>>>>>> d889270 (apply gitignore properly)
            u.first_name,
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
        WHERE p.seller_id = %s
        """
<<<<<<< HEAD
        params = [seller_id, seller_id]

        if search:
            sql += """
            AND (
                p.product_name LIKE %s
                OR p.description LIKE %s
                OR p.product_condition LIKE %s
            )
            """
            like = f"%{search}%"
            params.extend([like, like, like])

        self.cur.execute(sql, tuple(params))
        rows = self.cur.fetchall()

        return self._attach_image_url(rows)

    # -----------------------------
    # INTERNAL HELPER
    # -----------------------------
    def _attach_image_url(self, rows):
        """
        Converts DB image filename → usable Flask static URL
        """
        for row in rows:
            img = row.get("image_url")

            if img:
                # If it already has 'images/' prefix, use as-is
                # Otherwise prepend it
                if img.startswith('images/'):
                    row["image_url"] = img
                else:
                    row["image_url"] = f"images/{img}"
            else:
                row["image_url"] = "images/desk+chair.jpg"

        return rows
=======
        self.cur.execute(sql, (seller_id, seller_id))
        return self.cur.fetchall()
>>>>>>> d889270 (apply gitignore properly)
