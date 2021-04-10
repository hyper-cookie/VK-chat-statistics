import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("VKMessages.db")
        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
            message TEXT,
            user TEXT,
            date TEXT)
        """)
        self.connection.commit()

    def insert_data(self, message_value, user, date):
        self.cursor.execute("""INSERT INTO messages(
            message,
            user,
            date
            ) VALUES (?, ?, ?) 
        """, (message_value, user, date))
        self.connection.commit()

    def get_cursor(self):
        return self.cursor
