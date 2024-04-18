import telebot as tl
from data import db_session
from data.appointments import Appointments
from data.category import Category, create_category
from data.images import Images
from data.users import Users, Masters, Clients
from data.services import Services

bot = tl.TeleBot("6778264892:AAFj1C5Sa_7OYViFp_71oiENscNNxEqOijw")
email = ''
db_session.global_init('db/db.sqlite')


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
    bot.register_next_step_handler(message, emaile)

@bot.message_handler(content_types=["text"])
def send_anytext(mass):
    chat_id = mass.chat.id



def emaile(message):
    email = message.text.strip()
    if email == '/start':
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        bot.register_next_step_handler(message, emaile)
    db_sess = db_session.create_session()
    if not ('@' in email and ('.com' in email or '.ru' in email)):
        bot.send_message(message.chat.id, f"<n>Попробуй ещё раз, ты ввел не почту</n>",
                         parse_mode="html")
        bot.register_next_step_handler(message, emaile)
    elif db_sess.query(Users).filter(Users.email == email).first():
        user = db_sess.query(Users).filter(Users.email == email).first()
        if user.type == 'Masters':
            bot.send_message(message.chat.id, f"Введи число,которое ты запомнил на странице сайта {email}",
                            parse_mode="html", reply_markup=keyboard_master())
        else:
            bot.send_message(message.chat.id, f"Введи число,которое ты запомнил на странице сайта {email}",
                             parse_mode="html", reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, f"Ты не зарегестрирован на сайте",
                         parse_mode="html")
        bot.send_message(message.chat.id, "Привет, введи свою электронную почту", parse_mode="html")
        bot.register_next_step_handler(message, emaile)


def master_id(message):
    master_id_db = int(message.text.strip())
    db_sess = db_session.create_session()
    entry = db_sess.query(Appointments).filter(Appointments.master_id == master_id_db)
    print(', '.join([repr(i) for i in entry]))
    bot.send_message(message.chat.id, ', '.join([repr(i) for i in entry]))


@bot.message_handler(commands=["Zapic"])
def adding_zapis():
    pass

def keyboard():
    markup = tl.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = tl.types.KeyboardButton('Записаться')
    btn2 = tl.types.KeyboardButton('Мои записи')
    btn3 = tl.types.KeyboardButton('/start')
    markup.add(btn1, btn2, btn3)
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
