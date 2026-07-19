from parsser_class import ParserOzon
from db.db_connection import DB_my_connection
import sqlite3 as sq
from push_to_google_sheets import GoogleSheet


def main():
    url_for_parser_brands_and_params = {
        'УШМ': 'https://www.ozon.ru/category/uglovye-shlifmashiny-bolgarki-9879/',
        'Шуруповерты': 'https://www.ozon.ru/category/shurupoverty-9858/',
        'Электродрели': 'https://www.ozon.ru/category/elektrodreli-9860/',
        'Перфораторы': 'https://www.ozon.ru/category/perforatory-9859/',
        'Электролобзики': 'https://www.ozon.ru/category/elektrolobziki-9861/',
        'Циркулярные_пилы': 'https://www.ozon.ru/category/diskovye-pily-10066/',
        'Сварочное_оборудование': 'https://www.ozon.ru/category/svarochnye-apparaty-10047/',
        'Штроборезы_и_бороздоделы': 'https://www.ozon.ru/category/shtroborezy-9891/',
        'Электрорубанки': 'https://www.ozon.ru/category/elektrorubanki-9862/',
        'Ленточные_шлифмашины': 'https://www.ozon.ru/category/lentochnye-shlifmashiny-9875/',
        'Вибрационные_шлифмашины': 'https://www.ozon.ru/category/vibratsionnye-shlifmashiny-9876/',
        'Реноваторы_МФИ': 'https://www.ozon.ru/category/renovatory-34121/',
        'Лазерные_уровни_нивелиры': 'https://www.ozon.ru/category/lazernye-urovni-niveliry-34693/',
    }

    num = ParserOzon(pages=500, rasdels=url_for_parser_brands_and_params)
    result = num.passer_from_url_without_params()

    # Use parameterized queries in DB_my_connection to prevent SQL injection
    DB_my_connection().insert_in_db_codes_html(my_dict=result)

    with sq.connect('db/parser_ozon.db') as con:
        cursor = con.cursor()
        # Parameterized query for security
        cursor.execute('SELECT card_code, review, price, rat, date FROM codes_html WHERE date = (SELECT max(date) FROM codes_html)')
        data = cursor.fetchall()
        gs = GoogleSheet()
        gs.append_data(value_range_body=data, range="Все цены!A1:E1")


if __name__ == '__main__':
    main()