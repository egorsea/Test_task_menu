import telebot
import datetime
import psycopg2
import schedule
import time
import threading
import os

TOKEN = '6068054556:AAGXnemAIHfr6xNlrHMjqt3X0xfxW5Ki-70'
bot = telebot.TeleBot(TOKEN)


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


def get_orders():
    # Функция получения просроченных заказов
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT ordernumber, deliverytime FROM orderbook WHERE deliverytime < %s",
        (datetime.date.today(),))
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders


def create_table():
    # Создание таблицы в БД PostgreSQL если она не создана
    try:
        conn = connect_db()
        sql_create_table_query = """CREATE TABLE IF NOT EXISTS telegrambot(
                id SERIAL,
                chat_id INT PRIMARY KEY,
                name VARCHAR(30),
                user_id INT,
                addtime TIMESTAMP)"""
        cur = conn.cursor()
        cur.execute(sql_create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        print('Ошибка подключения к базе данных')
        return False


def insert_user(chat_id, name, user_id):
    # Функция добавлению в БД юзера для рассылки
    conn = connect_db()
    cur = conn.cursor()
    time = datetime.datetime.now()
    cur.execute("""INSERT INTO telegrambot (chat_id, name, user_id, addtime)
                VALUES (%s, %s, %s, %s) ON CONFLICT (chat_id) DO NOTHING;""",
                (chat_id, name, user_id, time))
    conn.commit()
    cur.close()
    conn.close()
    print('Добавлен новый адрес для рассылки')
    return True


def delete_user(chat_id):
    # Функция удаления юзера из БД для рассылки
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM telegrambot WHERE chat_id=(%s)', (chat_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True


def get_users():
    # Функция получения просроченных заказов
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT id, chat_id FROM telegrambot')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


@ bot.message_handler(commands=['start'])
def start(message):
    # Приветствие
    mess = f'👋 Привет, {message.from_user.first_name}!\n'
    mess += 'Я бот для оповещения о просроченных заказах.\n'
    mess += 'Я создан для выполнения тестового задания!\n'
    mess += 'Для получения уведомлений выполните команду /subscribe'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@ bot.message_handler(commands=['subscribe'])
def subscribe(message):
    # Подписка на рассылку
    mess = 'Вы подписаны на уведомления просроченных заказах.\n'
    mess += 'Уведомления будут поступать каждый день в 10:00.\n'
    mess += 'Для отключения уведомлений введите /end'
    insert_user(message.chat.id,
                f'{message.from_user.first_name} {message.from_user.last_name}',
                message.from_user.id)
    bot.send_message(message.chat.id, mess, parse_mode='html')


@ bot.message_handler(commands=['end'])
def end(message):
    # Отписка от рассылки
    delete_user(message.chat.id)
    bot.send_message(message.chat.id, 'Вы отписаны от уведомлений',
                     parse_mode='html')


def send_orders_message(bot):
    # Отправка сообщения с просроченными заказами
    users = get_users()
    if len(users) > 0:
        time = datetime.datetime.now()
        print(time, ' Рассылка сообщений')
        orders = get_orders()
        for user in users:
            chat_id = user[1]
            if len(orders) == 0:
                bot.send_message(
                    chat_id, 'На сегодня просроченных заказов нет')
            else:
                message = "Список просроченных заказов:\n"
                for order in orders:
                    if len(message) > 3500:
                        bot.send_message(chat_id, message)
                    message += f'Заказ № {order[0]} - срок поставки {order[1]};\n'
                message += 'Для отключения уведомлений введите /end'
                bot.send_message(chat_id, message)


def schedule_messages():
    # Запускаем рассылку каждый день в 10:00
    # schedule.every(10).seconds.do(send_orders_message, bot=bot)
    schedule.every().day.at("10:00").do(send_orders_message, bot=bot)
    while True:
        schedule.run_pending()
        time.sleep(2)


def main():
    create_table()
    # Запуск потока рассылки сообщений
    thread = threading.Thread(target=schedule_messages)
    thread.start()

    # Запускаем бота
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
