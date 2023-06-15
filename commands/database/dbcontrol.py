import sqlite3 as sql
from environment.variable import *


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

    def get_user_info(self, user_id: int, user_name: str, user_language: str):
        self.db_cursor.execute(f"""
        SELECT {ID}, {NAME}, {WEALTH}, {SCORE}, {LANGUAGE}
        FROM {USERS}
        WHERE id = {user_id};""")
        i = self.db_cursor.fetchone()
        if i:
            data = {ID: i[0], NAME: i[1], WEALTH: i[2], SCORE: i[3], LANGUAGE: i[4]}
            return data.get(WEALTH)
        else:
            self.db_cursor.execute(f"""
            INSERT INTO users ({ID}, {NAME}, {WEALTH}, {SCORE}, {LANGUAGE})
            VALUES ({user_id}, "{user_name}", 0, 0, "{user_language}");""")
            return "usercreated"

    def ch_user_money(self, users: list, mode: str, value: int):
        if mode == ADD:
            self.db_cursor.execute(f"""
            SELECT {ID}, {NAME}, {WEALTH}, {SCORE}, {LANGUAGE}
            FROM {USERS}
            WHERE id = {users[0]};""")
            i = self.db_cursor.fetchone()
            if i:
                data = {ID: i[0], NAME: i[1], WEALTH: i[2] + value, SCORE: i[3], LANGUAGE: i[4]}
                self.db_cursor.execute(f"""
                UPDATE {USERS} SET
                wealth = {data.get(WEALTH)}
                WHERE id = {data.get(ID)};""")
                return "added", data.get(WEALTH)
            else:
                return "nouser", None

        elif mode == "set":
            self.db_cursor.execute(f"""
                                    SELECT id,
                                    name,
                                    wealth,
                                    score,
                                    language
                                    FROM users
                                    WHERE id = {users[0]};""")
            i = self.db_cursor.fetchone()
            if i:
                data = {"id": i[0], "name": i[1], "wealth": value, "score": i[3], "language": i[4]}
                self.db_cursor.execute(f"""
                                UPDATE users SET
                                wealth = {data.get("wealth")}
                                WHERE id = {data.get("id")};""")
                return "changed", None
            else:
                return "nouser", None

        elif mode == "move" and len(users) == 2:
            self.db_cursor.execute(f"""
            SELECT id, name, wealth, score, language
            FROM users
            WHERE id = {users[0]};""")
            i = self.db_cursor.fetchone()
            if i:
                data1 = {"id": i[0], "name": i[1], "wealth": i[2], "score": i[3], "language": i[4]}
            else:
                return "nouser1", None, None
            self.db_cursor.execute(f"""
            SELECT id, name, wealth, score, language
            FROM users
            WHERE id = {users[1]};""")
            i = self.db_cursor.fetchone()
            if i:
                data2 = {"id": i[0], "name": i[1], "wealth": i[2], "score": i[3], "language": i[4]}
            else:
                return "nouser2", None, None
            if data1.get("wealth") - value >= 0 and value > 0:
                self.ch_user_money([data1.get("id")], ADD, -value)
                self.ch_user_money([data2.get("id")], ADD, value)
                return "tansfered", data1, data2
            elif value <= 0:
                return "valueerror", None, None
            else:
                return "notenoughmoney", data1, None
        else:
            return None


DB = DataBase()
