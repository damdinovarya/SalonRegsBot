from .db_connection import db

class Master:
    def __init__(self):
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_master(self, user_id, spec, experience, schedule):
        self.cur.execute(
            "INSERT INTO masters(user_id, spec, experience, schedule) VALUES (?, ?, ?, ?);",
            (user_id, spec, experience, schedule)
        )
        self.con.commit()

    async def is_master(self, user_id):
        masters_ids = self.cur.execute("SELECT user_id FROM masters;").fetchall()
        if user_id in masters_ids:
            return True
        return False

    async def get_master_by_id_telegram(self, user_id):
        return self.cur.execute("SELECT * FROM masters WHERE user_id = ?;",
                                (user_id,)).fetchall()[[-1]]
