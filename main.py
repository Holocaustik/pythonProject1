from parsser_class import ParserOzon
from db.db_connection import DB_my_connection
import sqlite3 as sq
from push_to_google_sheets import GoogleSheet


def main():
    # Ссыли для парсера
    url_for_parser_brands_and_params = {
        'УШМ': 'https://www.ozon.ru/category/uglovye-shlifmashiny-bolgarki-9879/',
        'Шуруповерты': 'https://www.ozon.ru/category/shurupoverty-9858/',
        'Электродрели': 'https://www.ozon.ru/category/elektrodreli-9860/',
        'Перфораторы': 'https://www.ozon.ru/category/perforatory-9859/',
        'Электролобзики': 'https://www.ozon.ru/category/elektrolobziki-9861/',
        'Циркулярные_пилы': 'https://www.ozon.ru/category/diskovye-pily-10066/',
        # 'Аккумуляторные_отвертки': 'https://www.ozon.ru/category/akkumulyatornye-otvertki-9902/',
        # # 'Газонокосилки_и_триммеры': 'https://www.ozon.ru/category/gazonokosilki-i-trimmery-14695/',
        # # 'Электро_и_бензопилы_цепные': 'https://www.ozon.ru/category/elektro-i-benzopily-tsepnye-10065/',
        'Сварочное_оборудование': 'https://www.ozon.ru/category/svarochnye-apparaty-10047/',
        'Штроборезы_и_бороздоделы': 'https://www.ozon.ru/category/shtroborezy-9891/',
        # # 'Клеевые_пистолеты_строительные': 'https://www.ozon.ru/category/kleevye-pistolety-stroitelnye-36082/',
        'Электрорубанки': 'https://www.ozon.ru/category/elektrorubanki-9862/',
        'Ленточные_шлифмашины': 'https://www.ozon.ru/category/lentochnye-shlifmashiny-9875/',
        'Вибрационные_шлифмашины': 'https://www.ozon.ru/category/vibratsionnye-shlifmashiny-9876/',
        # # 'Полировальные_машины': 'https://www.ozon.ru/category/polirovalnye-mashiny-9878/',
        # # 'Эксцентриковые_шлифмашины': 'https://www.ozon.ru/category/ekstsentrikovye-shlifmashiny-9881/',
        # 'Электроточила': 'https://www.ozon.ru/category/elektrotochila-9882/',
        'Реноваторы_МФИ': 'https://www.ozon.ru/category/renovatory-34121/',
        'Лазерные_уровни_нивелиры': 'https://www.ozon.ru/category/lazernye-urovni-niveliry-34693/',
        # 'Отрезные_диски': 'https://www.ozon.ru/category/diski-otreznye-10116/',
        # 'ingco': 'https://www.ozon.ru/category/instrumenty-dlya-remonta-i-stroitelstva-9856/
        # ?category_was_predicted=true&from_global=true&text=ingco',
        # 'Наборы': 'https://www.ozon.ru/category/nabory-instrumentov-31107/',
        # 'Видеонаблюдение': 'https://www.ozon.ru/category/kamery-videonablyudeniya-15846/'

    }

    # Создаем экземпляр класса парсера
    num = ParserOzon(pages=500, rasdels=url_for_parser_brands_and_params)

    # Парси ресурс
    result = num.passer_from_url_without_params()

    DB_my_connection().insert_in_db_codes_html(my_dict=result)

    # Запись результата парсера без параметров в базу
    # DB_my_connection().insert_in_db_codes_html(result)
    #
    # Запись на Гугл лист
    with sq.connect('db/parser_ozon.db') as con:
        cursor = con.cursor()
        sql_query = f'SELECT card_code, review, price, rat, date  FROM codes_html WHERE date == (SELECT max(date) ' \
                    f'from codes_html) '
        data = cursor.execute(sql_query).fetchall()
        gs = GoogleSheet()
        gs.append_data(value_range_body=data, range="Все цены!A1:E1")


if __name__ == '__main__':
    main()
