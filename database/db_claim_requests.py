from .db_connection import db


class Claim:
    def __init__(self):
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_claim(self, user_id, master_id, service, date, time):
        self.cur.execute("INSERT INTO claims(user_id, master_id, service, date, time, state) VALUES (?, ?, ?, ?, ?, ?);",
                         (user_id, master_id, service, date, time, 0))
        self.con.commit()

    async def get_claim(self, user_id, master_id):
        return self.cur.execute("SELECT * FROM claims WHERE user_id = ? AND master_id = ?;",
                                (user_id, master_id)).fetchall()[-1]
