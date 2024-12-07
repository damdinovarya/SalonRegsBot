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
        Создает админа в таблице `admins`.

        :param user_id: Telegram ID админа.
        :return: None
        """
        self.cur.execute("INSERT INTO claims(user_id) VALUES (?);", (user_id,))
        self.con.commit()

    async def get_admin_by_id_telegram(self, person_id):
        """
        Возвращает админа по Telegram ID.

        :param person_id: Telegram ID админа.
        :return: Кортеж с данными админов.
        """
        return self.cur.execute("SELECT * FROM admins WHERE user_id = ?;", (person_id,)).fetchall()[-1]
