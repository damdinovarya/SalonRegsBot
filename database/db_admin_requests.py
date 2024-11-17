from .db_connection import db


class Admin:
    def __init__(self):
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_admin(self, user_id):
        self.cur.execute("INSERT INTO claims(user_id) VALUES (?);", (user_id,))
        self.con.commit()

    async def get_admin_by_id_telegram(self, person_id):
        return self.cur.execute("SELECT * FROM admins WHERE user_id = ?;", (person_id,)).fetchall()[-1]
