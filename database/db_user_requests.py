from .db_connection import db

class User:
    def __init__(self):
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_user(self, id_telegram, fullname, tnumber):
        self.cur.execute(
            "INSERT INTO users(id_telegram, fullname, tnumber) VALUES (?, ?, ?);", 
            (id_telegram, fullname, tnumber)
        )
        self.con.commit()

    async def update_user(self, id_telegram, fullname, tnumber):
        self.cur.execute(
            "UPDATE users SET fullname = ?, tnumber = ? WHERE id_telegram = ?;",
            (fullname, tnumber, id_telegram)
        )
        self.con.commit()

    async def get_user_by_id_telegram(self, id_telegram):
        return self.cur.execute("SELECT * FROM users WHERE id_telegram = ?;", (id_telegram,)).fetchall()[-1]

    async def get_users(self):
        return self.cur.execute("SELECT * FROM users").fetchall()