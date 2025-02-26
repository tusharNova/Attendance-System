import sqlite3

class clsDb():
    def __init__(self):
        super(clsDb, self).__init__()
        self.conn = sqlite3.connect("DB/attedanceSystem.db")
        self.cur = self.conn.cursor()

    def runSql(self , query):
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def selectSql(self ,query):
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
