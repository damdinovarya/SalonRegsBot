from .db_connection import db

class User:
    def __init__(self):
        self.cur = db.get_cursor()

    async def create_user(self, id_telegram, fullname, tnumber):
        self.cur.execute(
            "INSERT INTO users(id_telegram, fullname, tnumber) VALUES (?, ?, ?);", 
            (id_telegram, fullname, tnumber)
        )
        self.cur.commit()

    async def get_user(self, id_telegram):
        return self.cur.execute("SELECT * FROM users WHERE id_telegram = ?;", (id_telegram,)).fetchall()[-1]
    
