from .db_connection import db

class Claim:
    def __init__(self):
        self.cur = db.get_cursor()

    async def create_claim(self, event_id, person_id, identity_card):
        with self.cur:
            self.cur.execute("INSERT INTO claims(event_id, person_id, identity_card) VALUES (?, ?, ?);", 
                             (event_id, person_id, identity_card))

    async def get_claim(self, claim_id):
        cur = self.con.cursor()
        return cur.execute("SELECT * FROM claims WHERE id = ?;", (claim_id,)).fetchall()
