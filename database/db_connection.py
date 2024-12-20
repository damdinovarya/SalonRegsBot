import sqlite3 as sl


class Database:
    """
    Класс для управления подключением к базе данных SQLite и работы с ней.
    Позволяет подключаться к базе данных, создавать необходимые таблицы и предоставлять методы для получения
    соединения и курсора.
    """

    def __init__(self, db_name='data.db'):
        """
        Инициализация объекта базы данных.

        :param db_name:
        """
        self.con = None
        self.cur = None
        self.db_name = db_name

    async def connect(self):
        """
        Подключение к базе данных и создание необходимых таблиц.
        """
        self.con = sl.connect(self.db_name)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Создание необходимых таблиц в базе данных, если они не существуют.
        """
        with self.con:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    id_telegram BIGINT,
                    fullname TEXT,
                    tnumber TEXT
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS claims (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    master_id BIGINT,
                    service TEXT,
                    date TEXT,
                    time TEXT,
                    state INTEGER
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS workers (
                    id INTEGER PRIMARY KEY,
                    user_id BIGINT,
                    username TEXT,
                    staff_id BIGINT
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    user_id BIGINT,
                    state INTEGER
                );
            """)
            self.con.commit()

    def get_connection(self):
        """
        Возвращает текущее соединение с базой данных.

        :return: Текущее соединение с базой данных.
        """
        if self.con is None:
            raise ValueError("Database connection is not established. Call 'connect()' first.")
        return self.con

    def get_cursor(self):
        """
        Возвращает текущий курсор для выполнения запросов к базе данных.

        :return: Текущий курсор.
        """
        if self.cur is None:
            raise ValueError("Database cursor is not initialized. Call 'connect()' first.")
        return self.cur


# Создаём глобальный экземпляр базы данных
db = Database()
