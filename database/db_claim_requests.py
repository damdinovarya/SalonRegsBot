from .db_connection import db


class Claim:
    """
    Класс для управления заявками в базе данных.
    """
    def __init__(self):
        """
        Инициализация объекта Claim.
        Устанавливает соединение с базой данных и создает курсор для выполнения SQL-запросов.
        """
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_claim(self, user_id, master_id, service, date, time):
        """
        Создает новую заявку в таблице `claims`.

        :param user_id: ID пользователя, подающего заявку.
        :param master_id: ID мастера, которому направлена заявка.
        :param service: Услуга, указанная в заявке.
        :param date: Дата выполнения заявки.
        :param time: Время выполнения заявки.
        :return: None
        """
        self.cur.execute("INSERT INTO claims(user_id, master_id, service, date, time, state) VALUES (?, ?, ?, ?, ?, ?);",
                         (user_id, master_id, service, date, time, 0))
        self.con.commit()

    async def get_claim_by_master_and_service(self, user_id, master_id, service):
        """
        Возвращает заявку пользователя

        :param user_id: ID пользователя.
        :param master_id: ID мастера.
        :param service: Услуга, указанная в заявке.
        :return: Кортеж с данными заявки.
        """
        ans = self.cur.execute("SELECT * FROM claims WHERE user_id = ? AND master_id = ? AND service = ?;",
                                (user_id, master_id, service)).fetchall()
        return [] if ans == [] else ans[-1]

    async def get_claim_by_user_id(self, user_id):
        """
        Возвращает список заявок, поданных пользователем.

        :param user_id: Идентификатор пользователя.
        :return: Список кортежей с данными заявок.
        """
        return self.cur.execute("SELECT * FROM claims WHERE user_id = ?",
                                (user_id,)).fetchall()

    async def get_claim_by_id(self, id):
        """
        Возвращает заявку по ID заявки.

        :param id: ID заявки.
        :return: Кортеж с данными заявки.
        """
        ans = self.cur.execute("SELECT * FROM claims WHERE id = ?", (id,)).fetchall()
        return [] if ans == [] else ans[-1]
