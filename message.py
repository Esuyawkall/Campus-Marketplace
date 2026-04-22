from baseObject import baseObject
class message(baseObject):
    def __init__(self):
        self.setup()

    def getMessagesByUserId(self, user_id):
        sql = """
        SELECT 
            u.user_id,
            u.first_name,
            u.last_name,
            u.email,
            m.message_text,
            m.date_sent
        FROM messages m
        JOIN users u 
            ON u.user_id = CASE 
                WHEN m.sender_id = %s THEN m.receiver_id
                ELSE m.sender_id
            END
        INNER JOIN (
            SELECT MAX(message_id) AS last_msg_id
            FROM messages
            WHERE sender_id = %s OR receiver_id = %s
            GROUP BY 
                CASE 
                    WHEN sender_id = %s THEN receiver_id
                    ELSE sender_id
                END
        ) latest
        ON m.message_id = latest.last_msg_id
        ORDER BY m.date_sent DESC;
        """
        self.cur.execute(sql, (user_id, user_id, user_id, user_id))
        return self.cur.fetchall()
    def getMessagesBetweenUsers(self, user1_id, user2_id, product_id=None):
        sql = """
        SELECT 
            m.message_id,
            m.sender_id,
            m.receiver_id,
            m.message_text,
            m.date_sent,
            m.product_id,
            u.first_name AS sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.user_id
        WHERE (m.sender_id = %s AND m.receiver_id = %s) 
           OR (m.sender_id = %s AND m.receiver_id = %s)
        """
        params = [user1_id, user2_id, user2_id, user1_id]
        
        if product_id:
            sql += " AND m.product_id = %s"
            params.append(product_id)
        
        sql += " ORDER BY m.date_sent ASC"
        self.cur.execute(sql, tuple(params))
        return self.cur.fetchall()
    def sendMessage(self, sender_id, receiver_id, message_text, product_id=None):
        sql = """
        INSERT INTO messages (sender_id, receiver_id, message_text, product_id, date_sent)
        VALUES (%s, %s, %s,%s, NOW())
        """ 
        self.cur.execute(sql, (sender_id, receiver_id, message_text, product_id))
        self.conn.commit()
    def deleteMessageById(self, message_id):
        sql = """
        DELETE FROM messages
        WHERE message_id = %s
        """ 
        self.cur.execute(sql, (message_id,))
        self.conn.commit()
    
    def getAllMessages(self):
        """Admin method to view all messages between all users"""
        sql = """
        SELECT 
            m.message_id,
            m.sender_id,
            m.receiver_id,
            m.message_text,
            m.date_sent,
            m.product_id,
            u1.first_name AS sender_name,
            u1.email AS sender_email,
            u2.first_name AS receiver_name,
            u2.email AS receiver_email,
            p.product_name
        FROM messages m
        JOIN users u1 ON m.sender_id = u1.user_id
        JOIN users u2 ON m.receiver_id = u2.user_id
        LEFT JOIN products p ON m.product_id = p.product_id
        ORDER BY m.date_sent DESC
        """
        self.cur.execute(sql)
        return self.cur.fetchall()