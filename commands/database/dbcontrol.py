import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def connect(self):
        self.db_connection = sql.connect("database.db")
        self.db_cursor = self.db_connection.cursor()

    def disconnect(self):
        self.db_connection.commit()
        self.db_connection.close()

    def get_user_info(self, user_id: int, user_name: str, user_language: str) -> dict:
        retry = 1
        while retry > 0:
            self.db_cursor.execute(f"""
            SELECT id,
            name,
            wealth,
            score,
            language
            FROM users
            WHERE id = {user_id};""")
            i = self.db_cursor.fetchone()
            if i:
                data = {
                    "id": i[0],
                    "name": i[1],
                    "wealth": i[2],
                    "score": i[3],
                    "language": i[4],
                }
                return data
            else:
                self.db_cursor.execute(f"""
                INSERT INTO users (
                id,
                name,
                wealth,
                score,
                language
                )
                VALUES (
                {user_id},
                {user_name},
                0,
                0,
                {user_language}
                );""")
                retry -= 1

    def ch_user_money(self, users: list, mode: str, value: int) -> None:
        if mode == "add":
            pass
        elif mode == "sub":
            pass
        elif mode == "set":
            pass
        elif mode == "move" and len(users) == 2:
            pass
        else:
            return None


DB = DataBase()
