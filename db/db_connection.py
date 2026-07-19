import sqlite3
import sqlite3 as sq


class DB_my_connection():
    def __init__(self, table_name=None):
        self.table_name = table_name

    def create_db(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    rasdel_name TEXT,
                    brand TEXT,
                    product_code INTEGER,
                    product_name TEXT,
                    product_link TEXT,
                    rew INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0,
                    product_stock INTEGER,
                    product_price INTEGER
                )""")

    def insert_in_db(self, data_list=None):
        if not data_list:
            return
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO codes
                           VALUES (
                           NULL, :date, :rasdel_name, :brand, :id, :name, :link, :rew, :rating, :stock, :price
                           )
                           """, data_list)
            con.commit()

    def create_table(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS params (id INTEGER PRIMARY KEY AUTOINCREMENT, radel TEXT, params TEXT)')
            con.commit()

    def insert_in_db_params(self, data_list):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany('INSERT INTO params VALUES (NULL, ?, ?)', data_list)
            con.commit()

    def create_table_with_params(self):
        if not self.table_name:
            return
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}_with_params (id INTEGER PRIMARY KEY AUTOINCREMENT)')

    def add_column(self, column):
        if not self.table_name:
            return
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            try:
                cursor.execute(f'ALTER TABLE {self.table_name}_with_params ADD COLUMN "{column}" TEXT')
            except sqlite3.OperationalError:
                pass
            else:
                con.commit()