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

    def insert_in_db(self, dict_data=None):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO codes
                           VALUES (
                           NULL,
                           :date,
                           :rasdel_name,
                           :brand,
                           :id,
                           :name,
                           :link,
                           :rew,
                           :rating,
                           :stock,
                           :price
                           )
                           """, dict_data)

            con.commit()

    def create_table(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_create_table = f'CREATE TABLE IF NOT EXISTS params (id INTEGER PRIMARY KEY AUTOINCREMENT, radel TEXT, params TEXT)'
            cursor.execute(text_for_create_table)
            con.commit()

    def insert_in_db_params(self, dict_data):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_insert_value_in_table = f'INSERT INTO params VALUES (NULL, ?, ?)'
            cursor.executemany(text_for_insert_value_in_table, dict_data)

            con.commit()

    def create_table_with_params(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_create_table = f'CREATE TABLE IF NOT EXISTS {self.table_name}_with_params (id INTEGER PRIMARY KEY AUTOINCREMENT)'
            cursor.execute(text_for_create_table)

    def add_column(self, column):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            try:
                new_text = f'ALTER TABLE {self.table_name}_with_params ADD COLUMN {column} TEXT'
                cursor.execute(new_text)
            except sqlite3.OperationalError:
                pass
            else:
                con.commit()

    def create_table_html(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS codes_html (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rasdel TEXT,
                    card_code INTEGER,
                    review INTEGER DEFAULT 0,
                    price INTEGER,
                    rat REAL,
                    date TEXT
                )""")

    def insert_in_db_codes_html(self, my_dict):
        self.create_table_html()
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO codes_html (rasdel, card_code, review, price, rat, date)
                           VALUES (:rasdel, :card_code, :review, :price, :rat, :date)
                           """, my_dict)
            con.commit()