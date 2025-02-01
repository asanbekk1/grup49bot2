import sqlite3

class Database:
    def __init__(self, db_name="db.sqlite3"):
        self.db_name = db_name

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homeworks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    homework_number TEXT,
                    github_link TEXT
                )
            """)
            conn.commit()

    def save_homework(self, username, homework_number, github_link):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO homeworks (username, homework_number, github_link)
                VALUES (?, ?, ?)
            """, (username, homework_number, github_link))
            conn.commit()
