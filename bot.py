from calendar import monthrange

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
month = ['январь',	'февраль',	'март',	'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
    bot.register_next_step_handler(message, emaile)


def emaile(message):
    global user, date_time
    email = message.text.strip()
    if email == '/start':
        user = ''
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        date_time = []
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


@bot.message_handler(content_types=["text"])
def mess(message):
    global date_time, user
    chat_id = message.chat.id
    if message.text == '/start':
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        date_time = []
        bot.register_next_step_handler(message, emaile)
    if user != '':
        if user.type == 'Clients':
            if message.text == 'Записаться':
                bot.send_message(message.chat.id, f"{user.nick_name}, введите число, которое вы запомнили на странице сайта, если вы не помните нажмите на 'Выбрать мастера' и найдите Nick name мастера в списке",
                                 parse_mode="html", reply_markup=keyboard())
                bot.register_next_step_handler(message, adding_zapis)
            if message.text == 'Выбрать мастера':
                master_id(chat_id)
                bot.register_next_step_handler(message, adding_zapis)
            if message.text == 'Удалить запись':
                t = my_zapis(user.type)
                if '\n'.join(t) == '':
                    bot.send_message(message.chat.id,
                                     'У вас не записей на ближайшее время', reply_markup=keyboard())
                else:
                    bot.send_message(message.chat.id,
                                     '\n'.join(t), reply_markup=keyboard())
                    bot.send_message(message.chat.id,
                                     'Введите номер записи, которую хотите удалить', reply_markup=keyboard())
                    bot.register_next_step_handler(message, delete_zapis)
            if message.text == 'Мои записи':
                t = my_zapis(user_type=user.type)
                if '\n'.join(t) == '':
                    bot.send_message(message.chat.id,
                                     'У вас не записей на ближайшее время', reply_markup=keyboard())
                else:
                    bot.send_message(message.chat.id,
                                     'Ваши записи', reply_markup=keyboard())
                    bot.send_message(message.chat.id,
                                     '\n'.join(t), reply_markup=keyboard())
        else:
            if message.text == 'Записи на сегодня' or message.text == 'Записи на 10 дней':
                t = my_zapis(user.type, 'now')
                if '\n'.join(t) == '':
                    bot.send_message(message.chat.id,
                                     'У вас не записей на ближайшее время', reply_markup=keyboard_master())
                else:
                    bot.send_message(message.chat.id,
                                     '\n'.join(t), reply_markup=keyboard_master())
    else:
        bot.send_message(message.chat.id,
                         'Ввойдите в систему, для этого нажмите /start', reply_markup=keyboard_start())


def my_zapis(user_type, date=''):
    db_sess = db_session.create_session()
    t = []
    if user_type == 'Clients':
        appoint = db_sess.query(Appointments).filter(user.id == Appointments.client_id)
        for item in appoint:
            if item.date >= datetime.datetime.today().date():
                if item.date == datetime.datetime.today().date() and item.time >= datetime.datetime.today().time():
                    r = f'{item.id} - {db_sess.query(Services).filter(Services.id == item.service_id).first().name} - {db_sess.query(Masters).filter(Masters.id == item.master_id).first().nick_name} - {item.date} - {item.time}'
                    t.append(r)
                elif item.date >= datetime.datetime.today().date():
                    r = f'{item.id} - {db_sess.query(Services).filter(Services.id == item.service_id).first().name} - {db_sess.query(Masters).filter(Masters.id == item.master_id).first().nick_name} - {item.date} - {item.time}'
                    t.append(r)
                else:
                    db_sess.delete(item)
                    db_sess.commit()
            else:
                db_sess.delete(item)
                db_sess.commit()
    else:
        if date == 'now':
            datee = datetime.datetime.today().date()
            appoint = db_sess.query(Appointments).filter(user.id == Appointments.master_id and Appointments.date == datee)
        else:
            datee = datetime.datetime.today().date()
            appoint = db_sess.query(Appointments).filter(
                user.id == Appointments.master_id and Appointments.date >= datee and Appointments.date <= (datee + datetime.timedelta(days=10)))
        for item in appoint:
            if item.date >= datetime.datetime.today().date():
                if item.date == datetime.datetime.today().date() and item.time >= datetime.datetime.today().time():
                    r = f'{item.id} - {db_sess.query(Services).filter(Services.id == item.service_id).first().name} - {db_sess.query(Clients).filter(Clients.id == item.client_id).first().nick_name} - {item.date} - {item.time}'
                    t.append(r)
                elif item.date >= datetime.datetime.today().date():
                    r = f'{item.id} - {db_sess.query(Services).filter(Services.id == item.service_id).first().name} - {db_sess.query(Clients).filter(Clients.id == item.client_id).first().nick_name} - {item.date} - {item.time}'
                    t.append(r)
                else:
                    db_sess.delete(item)
                    db_sess.commit()
            else:
                db_sess.delete(item)
                db_sess.commit()
    return t


def delete_zapis(mass):
    db_sess = db_session.create_session()
    entr = db_sess.query(Appointments).filter(Appointments.id == int(mass.text)).first()
    db_sess.delete(entr)
    db_sess.commit()
    bot.send_message(mass.chat.id,
                     'Вы успешно удалили запись')


def master_id(mass):
    db_sess = db_session.create_session()
    masters = db_sess.query(Masters).all()
    print('\n'.join([repr(i) for i in masters]))
    bot.send_message(mass, '\n'.join([repr(i) for i in masters]))


def adding_zapis(mass):
    global date_time
    if ''.join([i for i in mass.text if i in '1234567890']) == mass.text:
        db_sess = db_session.create_session()
        entry = db_sess.query(Appointments).filter(Appointments.master_id == int(mass.text) and datetime.date.today() <= Appointments.date and datetime.datetime.time() <= Appointments.time)
        date_time.append(int(mass.text))
        print('\n'.join([repr(i) for i in entry]))
        bot.send_message(mass.chat.id, 'Введите год на которое хотите записаться')
        bot.register_next_step_handler(mass, year)
    else:
        sortede(mass)



def servis(mass):
    global date_time, user
    db_sess = db_session.create_session()
    print(date_time[0], user.id)
    entryy = Appointments()
    entryy.master_id = date_time[0]
    entryy.client_id = user.id
    entryy.service_id = int(mass.text)
    entryy.date = datetime.date(date_time[1], date_time[2], date_time[3])
    entryy.time = datetime.time(*[int(i) for i in date_time[4].split(':')])
    db_sess.add(entryy)
    db_sess.commit()
    bot.send_message(mass.chat.id,
                     f'Вы удачно записались: на услугу {db_sess.query(Services).filter(Services.id == int(mass.text)).first().name}'
                     f' на {datetime.date(date_time[1], date_time[2], date_time[3])} в {date_time[4]} мастер будет ожидать вас по адресу:'
                     f' {db_sess.query(Masters).filter(Masters.id == date_time[0]).first().address}',
                     reply_markup=keyboard())
    date_time = []

def sortede(mass):
    global date_time
    if mass.text == '/start':
        bot.send_message(mass.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        date_time = []
        bot.register_next_step_handler(mass, emaile)
    if mass.text == 'Изменить дату':
        bot.send_message(mass.chat.id, 'Введите число на которое хотите записаться')
        bot.register_next_step_handler(mass, date)
    elif mass.text == 'Изменить месяц':
        bot.send_message(mass.chat.id, 'Введите месяц, на который хотите записаться', reply_markup=keyboard_mounth())
        del date_time[2]
        bot.register_next_step_handler(mass, mounth)
    if mass.text == 'Записаться':
        bot.send_message(mass.chat.id,
                         f"{user.nick_name}, введите число, которое вы запомнили на странице сайта, если вы не помните нажмите на 'Выбрать мастера' и найдите Nick name мастера в списке",
                         parse_mode="html", reply_markup=keyboard())
        bot.register_next_step_handler(mass, adding_zapis)
    if mass.text == 'Выбрать мастера':
        master_id(mass.chat.id)
        bot.register_next_step_handler(mass, adding_zapis)
    else:
        bot.register_next_step_handler(mass, sortede)


def date(mass):
    global date_time, month
    if datetime.date.today().day > int(mass.text) and date_time[2] == datetime.date.today().month:
        bot.send_message(mass.chat.id,
                         f'Вы не можете записаться на число, которое уже прошло, выберете другое или измените месяц. Выбранный месяц: {month[date_time[2] - 1]}',
                         reply_markup=adding_izmen())
        bot.register_next_step_handler(mass, sortede)
    elif monthrange(date_time[1], date_time[2])[1] < int(mass.text) or int(mass.text) < 1:
        bot.send_message(mass.chat.id,
                         'Вы не можете записаться на число, которого нет в выбранном вами месяце, введите другоеили измените месяц. Выбранный месяц: {month[date_time[2] - 1]}',
                         reply_markup=adding_izmen())
        bot.register_next_step_handler(mass, sortede)
    else:
        date_time.append(int(mass.text))
        bot.send_message(mass.chat.id, 'Введите время на которое хотите записаться в формате 12:10')
        bot.register_next_step_handler(mass, time)

def mounth(mass):
    global date_timem, month
    date_time.append(month.index(mass.text) + 1)
    bot.send_message(mass.chat.id, 'Введите число на которое хотите записаться')
    bot.register_next_step_handler(mass, date)

def year(mass):
    global date_time
    print(datetime.date.today().year)
    if int(mass.text) != int(datetime.date.today().year):
        bot.send_message(mass.chat.id, 'К сожалению нельзя записаться на год вперед, поэтому укажите текущий год')
        bot.register_next_step_handler(mass, year)
    else:
        date_time.append(int(mass.text))
        bot.send_message(mass.chat.id, 'Введите месяц, на который хотите записаться', reply_markup=keyboard_mounth())
        bot.register_next_step_handler(mass, mounth)

def time(mass):
    global date_time
    if datetime.datetime(date_time[1], date_time[2], date_time[3], *[int(i) for i in mass.text.split(':')]) >= datetime.datetime.now():
        date_time.append(mass.text)
        db_sess = db_session.create_session()
        servise = db_sess.query(Services).filter(Services.master_id == int(date_time[0]))
        bot.send_message(mass.chat.id, 'Введите номер услуги, на которую хотите записаться')
        bot.send_message(mass.chat.id, f'\n'.join([repr(i) for i in servise]), reply_markup=keyboard())
        bot.register_next_step_handler(mass, servis)
    else:
        bot.send_message(mass.chat.id, 'Введите новое время, на которое хотите записаться в формате 12:10, запись на ранее указанное вами время не возможно', reply_markup=keyboard())
        bot.register_next_step_handler(mass, time)




def keyboard():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = tl.types.KeyboardButton('Записаться')
    btn2 = tl.types.KeyboardButton('Мои записи')
    btn4 = tl.types.KeyboardButton('Выбрать мастера')
    btn5 = tl.types.KeyboardButton('Удалить запись')
    btn3 = tl.types.KeyboardButton('/start')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def keyboard_master():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = tl.types.KeyboardButton('Записи на сегодня')
    btn2 = tl.types.KeyboardButton('Записи на 10 дней')
    btn3 = tl.types.KeyboardButton(text='/start')
    markup.add(btn1, btn2, btn3)
    return markup

def keyboard_mounth():
    global month
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for moun in month[datetime.date.today().month - 1:]:
        btn1 = tl.types.KeyboardButton(moun)
        markup.add(btn1)
    return markup


def adding_izmen():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = tl.types.KeyboardButton('Изменить дату')
    btn1 = tl.types.KeyboardButton('Изменить месяц')
    markup.add(btn, btn1)
    return markup


def keyboard_start():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = tl.types.KeyboardButton('/start')
    markup.add(btn)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True)
