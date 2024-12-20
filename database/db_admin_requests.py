from .db_connection import db


class Admin:
    """
    Класс для управления админами в базе данных.
    Позволяет добавлять админов и получать информацию о них.
    """
    def __init__(self):
        """
        Инициализация объекта Admin.
        Устанавливает соединение с базой данных и создает курсор для выполнения SQL-запросов.
        """
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_admin(self, user_id):
        """
        Создает админа в таблице `admins` и задает статус 'требует подтверждения'.

        :param user_id: Telegram ID админа.
        :return: None
        """
        self.cur.execute("INSERT INTO admins(user_id, state) VALUES (?, ?);", (user_id, 0,))
        self.con.commit()

    async def accept_admin(self, user_id):
        """
        Меняет статус заявки админа на 'одобрена'.

        :param user_id: Telegram ID админа.
        :return: None
        """
        self.cur.execute("UPDATE admins SET state = ? WHERE user_id = ?;", (1, user_id,))
        self.con.commit()

    async def reject_admin(self, user_id):
        """
        Меняет статус заявки админа на 'отклонена'.

        :param user_id: Telegram ID админа.
        :return: None
        """
        self.cur.execute("UPDATE admins SET state = ? WHERE user_id = ?;", (3, user_id,))
        self.con.commit()

    async def delete_admin(self, user_id):
        """
        Меняет статус админа на 'бывший'.

        :param user_id: Telegram ID админа.
        :return: None
        """
        self.cur.execute("UPDATE admins SET state = ? WHERE user_id = ?;", (2, user_id,))
        self.con.commit()

    async def get_admin_by_id_telegram(self, person_id):
        """
        Возвращает админа по Telegram ID.

        :param person_id: Telegram ID админа.
        :return: Кортеж с данными админов.
        """
        ans = self.cur.execute("SELECT * FROM admins WHERE user_id = ?;", (person_id,)).fetchall()
        return [] if ans == [] else ans[-1]

    async def get_all_admins(self):
        """
        Возвращает активных админов по Telegram ID.

        :param person_id: Telegram ID админа.
        :return: Кортеж с данными админов.
        """
        ans = self.cur.execute("SELECT * FROM admins WHERE state = 1;").fetchall()
        return [] if ans == [] else ans
