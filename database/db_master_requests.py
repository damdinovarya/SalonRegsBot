from .db_connection import db

class Master:
    def __init__(self):
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_person(self, user_id, spec, experience, schedule):
        self.cur.execute(
            "INSERT INTO masters(user_id, spec, experience, schedule) VALUES (?, ?, ?, ?);",
            (user_id, spec, experience, schedule)
        )
        self.con.commit()

    async def is_master(self, user_id):
        row = self.cur.execute("SELECT user_id FROM masters;").fetchall()
        print(row)
