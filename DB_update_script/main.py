import schedule
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from xml.etree import ElementTree
import psycopg2
from datetime import datetime
from decimal import Decimal
import os


def get_usd_rate():
    # функция для получения курса доллара
    global usd_rate
    # usd_rate = 76
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)

    USD_VALUTE_ID = 'R01235'

    root = ElementTree.fromstring(response.content)
    for valute in root:
        if valute.attrib['ID'] == USD_VALUTE_ID:
            usd_rate = round(
                float(valute.find('Value').text.replace(',', '.')), 2)
            break
    # print('Курс доллара: ', usd_rate)
    return usd_rate


def connect_db():
    # Подключение к БД
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        port=5432,
        dbname='canalservis',
        user='dev',
        password='canalservis'
    )
    return conn


def create_table():
    # Создание таблицы в БД PostgreSQL если она не создана
    try:
        conn = connect_db()
        sql_create_table_query = """CREATE TABLE IF NOT EXISTS orderbook(
            orderbook_id INT,
            ordernumber INT PRIMARY KEY,
            price INT,
            deliverytime DATE,
            price_rub NUMERIC(10, 2))"""
        cur = conn.cursor()
        cur.execute(sql_create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        print('Ошибка подключения к базе данных')
        return False


def upload_to_DB(rows):
    # Функция добавления данных в базу
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM orderbook")
        prev_rows = cur.fetchall()
        prev_rows = [list(row) for row in prev_rows]

        if prev_rows != rows:
            print('Обновление данных в базе')
            cur.execute('DELETE FROM orderbook')
            for row in rows:
                cur.execute("INSERT INTO orderbook (orderbook_id, ordernumber, price, deliverytime, price_rub) VALUES (%s, %s, %s, %s, %s)",
                            (row[0], row[1], row[2], row[3], row[4]))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        print('Ошибка подключения к базе данных')
        return False


def main():

    usd_rate = get_usd_rate()
    schedule.every().hour.at('00:00').do(get_usd_rate)

    # Настройки доступа к таблице Google Sheets
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', SCOPES)
    SPREADSHEET_ID = '10TOzm7aCafSypgnKu6xH3u4DhJs9VkMbp1WYa1iIofQ'
    SHEET_NAME = 'Лист1'

    create_table()

    while True:
        rows = []
        # Получение данных из Google Sheets
        client = gspread.authorize(credentials)
        worksheet = client .open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        rows = worksheet.get_all_values()
        rows.pop(0)

        table = []
        for index, row in enumerate(rows):
            row = row[:4]

            # Несколько проверок что введены правильные данные
            if row[1].isdigit():
                row[1] = int(row[1])
            else:
                print(
                    f'Неверные данные в строке {index+2}, строка игнорируется')
                continue    # пропускаем строку, столбец "номер заказа" должен быть заполнен

            if row[0].isdigit():
                row[0] = int(row[0])
            else:
                row[0] = None
                print(f'Не верно указан ID в строке {index+2}')

            if row[2].isdigit():
                row[2] = int(row[2])
                row.append(
                    Decimal(str(int(row[2])*usd_rate)).quantize(Decimal('.01')))
            else:
                row[2] = None
                row.append(None)
                print(f'Не верно указана стоимость в строке {index+2}')

            try:
                row[3] = datetime.strptime(row[3], '%d.%m.%Y').date()
            except ValueError:
                print(f'Неверная дата в строке {index+2}')
                row[3] = None

            # собираем результат фильтрации и приведения типов
            table.append(row)

        upload_to_DB(table)

        schedule.run_pending()

        time.sleep(10)


if __name__ == '__main__':
    main()
