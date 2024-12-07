import sqlite3 as sl


class Database:
    """Подключение к базе данных и создание необходимых таблиц, если они не существуют"""

    def __init__(self, db_name='data.db'):
        self.con = None
        self.cur = None
        self.db_name = db_name

    async def connect(self):
        """Подключение к базе данных"""
        self.con = sl.connect(self.db_name)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        """Создаёт необходимые таблицы в базе данных"""
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
                    master_id INTEGER
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    user_id BIGINT
                );
            """)
            self.con.commit()

    def get_connection(self):
        """Возвращает текущее подключение к БД"""
        if self.con is None:
            raise ValueError("Database connection is not established. Call 'connect()' first.")
        return self.con

    def get_cursor(self):
        """Возвращает общий курсор для выполнения запросов к БД"""
        if self.cur is None:
            raise ValueError("Database cursor is not initialized. Call 'connect()' first.")
        return self.cur


# Создаём глобальный экземпляр базы данных
db = Database()
