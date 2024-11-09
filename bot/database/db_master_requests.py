from .db_connection import db

class Master:
    def __init__(self):
        self.con = db.get_connection()

    async def create_person(self, name, person_id, username, work_or_education, mail, claims):
        with self.con:
            self.con.execute(
                "INSERT INTO people(person_name, person_id, username, work_or_education, mail, claims) VALUES (?, ?, ?, ?, ?, ?);", 
                (name, person_id, username, work_or_education, mail, claims)
            )

    async def get_person_by_id(self, person_id):
        cur = self.con.cursor()
        return cur.execute("SELECT * FROM people WHERE person_id = ?;", (person_id,)).fetchall()