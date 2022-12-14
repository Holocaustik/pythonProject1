from __future__ import annotations
import datetime
import json
from browser import Driver_Chrom
import time
import pandas as pd
import sqlite3 as sq
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class ParserOzon(object):

    def __init__(self, pages: int = 2, rasdels=None):
        self.pages = pages
        self.rasdels = rasdels

    # Находит классы для страниц, с одной карточкой в столбце
    def get_classes_USM(self) -> dict:
        driver = Driver_Chrom().loadChrome()
        url = 'https://www.ozon.ru/category/uglovye-shlifmashiny-bolgarki-9879/'
        driver.get(url)
        time.sleep(1)
        name_class_find = driver.find_element("xpath", '//span[contains(text(), "Углошлифовальная машина")]')
        link_class = driver.find_element("xpath", '//a[contains(@class, "tile-hover-target")]').get_attribute('class').split()[1]
        name_class = driver.find_element("xpath", '//span[contains(text(), "Углошлифовальная машина")]//preceding::span[1]').get_attribute('class')
        main_div = driver.find_element("xpath", '//span[contains(text(), "Углошлифовальная машина")]//ancestor::div[3]')
        main_cards_class = main_div.get_attribute('class')
        price_class = main_div.find_element("xpath", '//span[contains(text(), "₽")]').get_attribute('class').split()[0]
        review_class_up = main_div.find_element("xpath", '//a[contains(text(), "отзывов")]')
        review_class = review_class_up.get_attribute('class')
        rat_class = main_div.find_element("xpath", '//a[contains(text(), "отзывов")]//preceding::div[1]').get_attribute('class')
        divs_class = {'main_cards_class': main_cards_class, 'price_class': price_class, 'review_class': review_class,'rat_class': rat_class, 'link_class': link_class}
        driver.close()
        driver.quit()
        print(main_cards_class)
        return divs_class

    # Находит классы для страниц, с четырьмя карточками в столбце
    def get_class_shurupovert(self) -> dict:
        url = 'https://www.ozon.ru/category/shurupoverty-9858/'
        driver = Driver_Chrom().loadChrome()
        driver.get(url)
        time.sleep(1)
        name_class_find = driver.find_element("xpath", '//span[contains(text(), "Шуруповерт аккумуляторный")]')
        link_class = driver.find_element("xpath", '//a[contains(@class, "tile-hover-target")]').get_attribute('class').split()[1]
        name_class = name_class_find.get_attribute('class')
        main_div = driver.find_element("xpath", '//span[contains(text(), "Шуруповерт аккумуляторный")]//ancestor::div[2]')
        main_cards_class = main_div.get_attribute('class')
        price_class = main_div.find_element("xpath", '//span[contains(text(), "₽")]').get_attribute('class').split()[0]
        review_class_up = main_div.find_element("xpath", '//a[contains(text(), "отзывов")]')
        review_class = review_class_up.get_attribute('class')
        rat_class = main_div.find_element("xpath", '//a[contains(text(), "отзывов")]//preceding::div[1]').get_attribute('class')
        divs_class = {'main_cards_class': main_cards_class, 'price_class': price_class,'review_class': review_class, 'rat_class': rat_class, 'link_class': link_class}
        driver.close()
        driver.quit()
        print(main_cards_class)
        return divs_class

    def passer_from_url_without_params(self) -> list:
        divs_shurupovert, divs_usm = self.get_class_shurupovert(), self.get_classes_USM()
        date = datetime.date.today().strftime('%d. %m. %Y')
        result = []
        set_cards_code = set()
        for key, url in self.rasdels.items():
            check_end_page = 0
            divs_class = divs_usm if key == 'УШМ' or key == 'Видеонаблюдение' else divs_shurupovert
            main_cards_class = divs_class['main_cards_class']
            link_class = divs_class['link_class']
            price_class = divs_class['price_class']
            review_class = divs_class['review_class']
            rat_class = divs_class['rat_class']
            driver = Driver_Chrom().loadChrome()
            driver.get(f'{url}')
            for page in range(1, self.pages + 1):
                print(f'Парсим {key} page {page}')
                if check_end_page < 6:
                    time.sleep(1.0)
                    find_class = f'//div[contains(@class, "{main_cards_class}")]'
                    divs = driver.find_elements("xpath", find_class)
                    print(len(divs))
                    if len(divs) > 4:
                        for div in divs:
                            link_pre = div.find_element(By.CLASS_NAME, link_class).get_attribute('href')
                            card_code = link_pre[:link_pre.find('?') - 1].split('-')[-1] if len(link_pre[:link_pre.find('?') - 1].split('-')[-1]) < 10 else link_pre[:link_pre.find('?') - 1].split('/')[-1]
                            if card_code not in set_cards_code:
                                set_cards_code.add(card_code)
                                try:
                                    price = int(div.find_element(By.CLASS_NAME, price_class).text.replace('\u2009', '').replace('\n', '').split('₽')[0])
                                except:
                                    price = int(div.find_element(By.XPATH, "//span[contains(text(), '₽')]").text.replace('\u2009', '').replace('\n', '').replace(' ', '').split('₽')[0])
                                try:
                                    review = div.find_element(By.CLASS_NAME, review_class).text.split()[0]
                                except:
                                    review = 0
                                try:
                                    rat = ''.join(div.find_element(By.CLASS_NAME, rat_class).get_attribute('style').replace('width:', '').replace('%;', '').split())
                                except:
                                    rat = 0
                                result.append({
                                    'rasdel': key,
                                    'card_code': card_code,
                                    'review': review,
                                    'price': price,
                                    'rat': rat,
                                    'date': date
                                })
                            else:
                                print('Такой код уже есть')
                    else:
                        print('Не нашли карточки')
                        check_end_page += 1
                        print(check_end_page)
                else:
                    print('Сработал флаг')
                    break
                try:
                    action = ActionChains(driver)
                    button = driver.find_element("xpath", '//div[contains(text(), "Дальше")]')
                    action.move_to_element(to_element=button).click().perform()
                except:
                    print('Не нашли кнопку')
                    check_end_page += 1
            driver.close()
            driver.quit()
        return result

    def parser_with_params(self) -> list:
        unick_params = set()
        for rasdel in self.rasdels:
            print(rasdel)
            with sq.connect('db/parser_ozon.db') as con:
                cursor = con.cursor()
                num = 'codes_html'
                sql_url = f'SELECT DISTINCT card_code FROM {num} WHERE rasdel == "{rasdel}"'
                open_file = cursor.execute(sql_url).fetchall()[:5]
                print(f'Всего будет записано {len(open_file)} карточкек')
            list_of_products = []
            caunter = 0
            for product in open_file:
                caunter += 1
                product_code = product[0]
                url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/product/{product_code}&layout_container=pdpPage2column&layout_page_index=2'
                driver = Driver_Chrom().loadChrome()
                driver.get(url)
                time.sleep(random.uniform(3, 1))
                try:
                    result = json.loads(driver.page_source.strip('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))
                    num = result['widgetStates']
                    for i in num:
                        if 'webCurrentSeller' in i:
                            saler_id_class = i
                    saler = json.loads(result['widgetStates'][saler_id_class])
                except:
                    pass
                try:
                    key_params = list(filter(lambda x: 'webCharacteristics' in x, result['widgetStates']))[0]
                    product_info = json.loads(result['widgetStates'][key_params])["characteristics"][0]['short']
                    name = str(json.loads(result['widgetStates'][key_params])["productTitle"]).strip('Характеристики: ')
                    sales_id = saler['id']
                    sales_name = saler['name']
                    sales_credentials = saler['credentials']
                    params = {}
                    for param in product_info:
                        unick_params.add(param["name"])
                        params[param["name"]] = param["values"][0]["text"]
                    list_of_products.append({
                        'code': product_code,
                        'name': name,
                        'sales_id': sales_id,
                        'sales_name': sales_name,
                        'sales_credentials': sales_credentials,
                        'params': params
                    })
                except:
                    pass
            return list_of_products

    def parser_params(self, rasdel) -> list:
        unick_params = set()
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            num = 'codes'
            sql_url = f'SELECT product_code FROM {num} WHERE rasdel_name == "{rasdel}"'
            open_file = cursor.execute(sql_url)
        for product in open_file:
            product_code = product[0]
            url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/product/{product_code}&layout_container=pdpPage2column&layout_page_index=2'
            driver = Driver_Chrom().loadChrome()
            driver.get(url)
            time.sleep(0.25)
            try:
                result = json.loads(driver.page_source.strip(
                    '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))
            except:
                pass
            try:
                key_params = list(filter(lambda x: 'webCharacteristics' in x, result['widgetStates']))[0]
                product_info = json.loads(result['widgetStates'][key_params])["characteristics"][0]['short']
                for param in product_info:
                    unick_params.add(param["name"])
            except:
                pass
        return list(map(lambda x: tuple([rasdel, x]), unick_params))

    def parser_with_params_little(self) -> list:
        unick_params = set()
        list_of_products = []
        for rasdel in self.rasdels:
            print(rasdel)
            with sq.connect('db/parser_ozon.db') as con:
                cursor = con.cursor()
                num = 'codes_html'
                sql_url = f'SELECT DISTINCT card_code FROM {num} WHERE rasdel == "{rasdel}"'
                open_file = cursor.execute(sql_url).fetchall()[:2]
                print(f'Всего будет записано {len(open_file)} карточкек')
            caunter = 0
            for product in open_file:
                caunter += 1
                product_code = product[0]
                url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/product/{product_code}&layout_container=pdpPage2column&layout_page_index=2'
                driver = Driver_Chrom().loadChrome()
                driver.get(url)
                time.sleep(random.uniform(3, 1))
                try:
                    result = json.loads(driver.page_source.strip('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))
                    num = result['widgetStates']
                    for i in num:
                        if 'webCurrentSeller' in i:
                            saler_id_class = i
                    saler = json.loads(result['widgetStates'][saler_id_class])
                except:
                    pass
                try:
                    key_params = list(filter(lambda x: 'webCharacteristics' in x, result['widgetStates']))[0]
                    product_info = json.loads(result['widgetStates'][key_params])["characteristics"][0]['short']
                    name = str(json.loads(result['widgetStates'][key_params])["productTitle"]).strip('Характеристики: ')
                    sales_id = saler['id']
                    sales_name = saler['name']
                    sales_credentials = saler['credentials']
                    for param in product_info:
                        unick_params.add(param["name"])
                        list_of_products.append((
                            rasdel,
                            product_code,
                            name,
                            sales_id,
                            sales_name,
                            ' '.join(sales_credentials),
                            param["name"],
                            param["values"][0]["text"]))
                except:
                    pass
        return list_of_products

    def parser_other_pages(self, url_in: str = None, brand: str = None, category: str = None) -> list:
        items = []
        for i in range(1, self.pages):
            if brand is None and category is None and url_in is not None:
                url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url={url_in}'
            if brand is None and category is None and url_in is None:
                print('Вы не указали что искать((')
            if brand is not None and category is not None:
                url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/{category}/?page={i}&text={brand}'
            if brand is None and category is not None:
                url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/{category}/?page={i}'
            driver = Driver_Chrom().loadChrome()
            driver.get(url)
            time.sleep(0.2)
            result = json.loads(driver.page_source.strip(
                '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))[
                'trackingPayloads']
            for key, val in result.items():
                num = json.loads(val)
                try:
                    testik = num['adv_second_bid']
                    id = num['id']
                    stockCount = num['stockCount']
                    final_price = num['finalPrice']
                    name = num['title']
                    index_for_link = str(num['link']).index('/?asb')
                    link = f'https://www.ozon.ru{str(num["link"])[:index_for_link]}'
                    items.append({
                        'id': id,
                        'name': name,
                        'link': link,
                        'stock': stockCount,
                        'price': final_price
                    })
                except:
                    pass
            time.sleep(random.randint(10, 6))
        return items

    def save_to_excel(self, data: list | dict | tuple = None, name='ozon'):
        num = pd.DataFrame(data)
        num.to_excel(f'{name}.xlsx')