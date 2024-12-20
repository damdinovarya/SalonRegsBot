from .db_connection import db


class Worker:
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

    async def create_worker(self, username, staff_id):
        """
        Создает сотрудника в таблице `workers`.

        :param username: Telegram username сотрудника.
        :return: None
        """
        self.cur.execute("INSERT INTO workers(user_id, username, staff_id) VALUES (?, ?, ?);", (-1, username, staff_id))
        self.con.commit()

    async def update_worker(self, user_id, username):
        """
        Добавляет Telegram id сотрудника в базу.

        :param user_id: Telegram ID админа.
        :param username: Telegram username админа.
        :return: None
        """
        self.cur.execute("UPDATE workers SET user_id = ? WHERE username = ?;", (user_id, username,))
        self.con.commit()


    async def update_worker_username(self, username, staff_id):
        """
        Добавляет Telegram id сотрудника в базу.

        :param user_id: Telegram ID админа.
        :param username: Telegram username админа.
        :param staff_id: YClients Staff ID сотрудника.
        :return: None
        """
        self.cur.execute("UPDATE workers SET user_id = ?, username = ? WHERE staff_id = ?;", (-1, username, staff_id))
        self.con.commit()


    async def get_worker_by_staff_id(self, staff_id):
        """
        Возвращает сотрудника по YClients Staff ID.

        :param staff_id: YClients Staff ID сотрудника.
        :return: Кортеж с данными сотрудников.
        """
        ans = self.cur.execute("SELECT * FROM workers WHERE staff_id = ?;", (staff_id,)).fetchall()
        return [] if ans == [] else ans[-1]


    async def get_worker_by_username(self, username):
        """
        Возвращает сотрудника по YClients Staff ID.

        :param username: Telegram username админа.
        :return: Кортеж с данными сотрудников.
        """
        ans = self.cur.execute("SELECT * FROM workers WHERE username = ?;", (username,)).fetchall()
        return [] if ans == [] else ans[-1]


    async def get_worker_by_user_id(self, user_id):
        """
        Возвращает сотрудника по Telegram ID.

        :param user_id: Telegram ID админа.
        :return: Кортеж с данными сотрудников.
        """
        ans = self.cur.execute("SELECT * FROM workers WHERE user_id = ?;", (user_id,)).fetchall()
        return [] if ans == [] else ans[-1]