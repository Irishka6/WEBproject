import telebot as tl
from data import db_session
from data.appointments import Appointments
from data.category import Category, create_category
from data.images import Images
from data.users import Users, Masters, Clients
from data.services import Services
import datetime

bot = tl.TeleBot("6778264892:AAFj1C5Sa_7OYViFp_71oiENscNNxEqOijw")
user = ''
db_session.global_init('db/db.sqlite')
date_time = []


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
    bot.register_next_step_handler(message, emaile)


def emaile(message):
    global user
    email = message.text.strip()
    if email == '/start':
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        bot.register_next_step_handler(message, emaile)
    db_sess = db_session.create_session()
    if not ('@' in email and ('.com' in email or '.ru' in email)):
        bot.send_message(message.chat.id, f"Попробуй ещё раз, ты ввел не почту",
                         parse_mode="html")
        bot.register_next_step_handler(message, emaile)
    else:
        if db_sess.query(Users).filter(Users.email == email).first():
            user = db_sess.query(Users).filter(Users.email == email).first()
            if user.type == 'Masters':
                bot.send_message(message.chat.id, f"{user.nick_name}, что вы хотели бы узнать",
                                parse_mode="html", reply_markup=keyboard_master())
            else:
                bot.send_message(message.chat.id, f"{user.nick_name}, что вы хотели бы узнать",
                                 parse_mode="html", reply_markup=keyboard())
        else:
            bot.send_message(message.chat.id, f"Ты не зарегестрирован на сайте",
                             parse_mode="html")
            bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
            bot.register_next_step_handler(message, emaile)
    if email == 'Записаться':
        bot.send_message(message.chat.id, f"{user.nick_name}, введите число, которое вы запомнили на странице сайта, если вы не помните нажмите на 'Выбрать мастера' и найдите Nick name мастера в списке",
                         parse_mode="html", reply_markup=keyboard())
    if email == 'Выбрать мастера':
        bot.register_next_step_handler(message, master_id)


@bot.message_handler(content_types=["text"])
def mess(message):
    chat_id = message.chat.id
    if message.text == '/start':
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        bot.register_next_step_handler(message, emaile)
    if message.text == 'Записаться':
        bot.send_message(message.chat.id, f"{user.nick_name}, введите число, которое вы запомнили на странице сайта, если вы не помните нажмите на 'Выбрать мастера' и найдите Nick name мастера в списке",
                         parse_mode="html", reply_markup=keyboard())
    if message.text == 'Выбрать мастера':
        master_id(chat_id)
        bot.register_next_step_handler(message, adding_zapis)


def master_id(mass):
    db_sess = db_session.create_session()
    masters = db_sess.query(Masters).all()
    print('\n'.join([repr(i) for i in masters]))
    bot.send_message(mass, '\n'.join([repr(i) for i in masters]))


def adding_zapis(mass):
    global date_time
    db_sess = db_session.create_session()
    entry = db_sess.query(Appointments).filter(Appointments.master_id == int(mass.text) and datetime.date.today() <= Appointments.date and datetime.datetime.time() <= Appointments.time)
    date_time.append(int(mass.text))
    print('\n'.join([repr(i) for i in entry]))
    bot.send_message(mass.chat.id, 'Введите год на которое хотите записаться')
    bot.register_next_step_handler(mass, year)
    # servis = db_sess.query(Services).filter(Services.master_id == int(mass.id))
    # bot.send_message(mass.chat.id, f'\n'.join([repr(i) for i in servis]))


def servis(mass):
    global date_time, user
    db_sess = db_session.create_session()
    entry = Appointments()
    entry.master_id = date_time[0]
    entry.client_id = user.id
    entry.service_id = int(mass.text)
    entry.date = datetime.date(date_time[1], date_time[2], date_time[3])
    entry.time = datetime.time(*[int(i) for i in date_time[4].split(':')])
    db_sess.add(entry)
    db_sess.commit()


def date(mass):
    global date_time
    date_time.append(int(mass.text))
    bot.send_message(mass.chat.id, 'Введите время на которое хотите записаться в формате 12:10')
    bot.register_next_step_handler(mass, time)

def mounth(mass):
    global date_time
    date_time.append(int(mass.text))
    bot.send_message(mass.chat.id, 'Введите число на которое хотите записаться')
    bot.register_next_step_handler(mass, date)

def year(mass):
    global date_time
    date_time.append(int(mass.text))
    bot.send_message(mass.chat.id, 'Введите месяц на которое хотите записаться')
    bot.register_next_step_handler(mass, mounth)

def time(mass):
    global date_time
    date_time.append(mass.text)
    bot.register_next_step_handler(mass, servis)




def keyboard():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = tl.types.KeyboardButton('Записаться')
    btn2 = tl.types.KeyboardButton('Мои записи')
    btn4 = tl.types.KeyboardButton('Выбрать мастера')
    btn3 = tl.types.KeyboardButton('/start')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def keyboard_master():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = tl.types.KeyboardButton('Записи на сегодня')
    btn2 = tl.types.KeyboardButton('Записи на следующие 10 дней')
    btn3 = tl.types.KeyboardButton(text='/start')
    markup.add(btn1, btn2, btn3)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True)
