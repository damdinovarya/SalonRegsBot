from .db_connection import db


class User:
    """
    Класс для управления пользователями в базе данных.
    """
    def __init__(self):
        """
        Инициализация объекта User.
        Устанавливает соединение с базой данных и создает курсор для выполнения SQL-запросов.
        """
        self.con = db.get_connection()
        self.cur = db.get_cursor()

    async def create_user(self, id_telegram, fullname, tnumber):
        """
        Создает нового пользователя в таблице `users`.

        :param id_telegram: Telegram ID пользователя.
        :param fullname: Имя пользователя.
        :param tnumber: Номер телефона пользователя.
        :return: None
        """
        self.cur.execute(
            "INSERT INTO users(id_telegram, fullname, tnumber) VALUES (?, ?, ?);",
            (id_telegram, fullname, tnumber)
        )
        self.con.commit()

    async def update_user(self, id_telegram, fullname, tnumber):
        """
        Обновляет информацию о пользователе.

        :param id_telegram: Telegram ID пользователя.
        :param fullname: Имя пользователя.
        :param tnumber: Номер телефона пользователя.
        :return: None
        """
        self.cur.execute(
            "UPDATE users SET fullname = ?, tnumber = ? WHERE id_telegram = ?;",
            (fullname, tnumber, id_telegram)
        )
        self.con.commit()

    async def get_user_by_id_telegram(self, id_telegram):
        """
        Возвращает информацию о пользователе.

        :param id_telegram: Telegram ID пользователя.
        :return: Кортеж с данными пользователя или None, если пользователь не найден.
        """
        return self.cur.execute("SELECT * FROM users WHERE id_telegram = ?;", (id_telegram,)).fetchall()[-1]

    async def get_users(self):
        """
        Возвращает список всех пользователей из таблицы `users`.

        :return: Список кортежей с данными пользователей.
        """
        return self.cur.execute("SELECT * FROM users").fetchall()
