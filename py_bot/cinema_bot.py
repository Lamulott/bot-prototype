import telebot
from telebot import types
import random
from classSite import Site
from csvReader import get_notes

url = 'https://www.baskino.re/'
headers = {
    'Accept': '*/*',
    'User_Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.731 Mobile Safari/537.36'
}
s = Site(url, headers)
films_for_today = s.get_total_list()
random.shuffle(films_for_today)

parting = ['До новых встреч!', 'До встречи!', 'Пока-пока!', 'До скорой встречи!', 'До следующей встречи!',
           'See you soon!']
random.shuffle(parting)
num = [i for i in range(len(parting))]

bot = telebot.TeleBot('6918194595:AAHo7WOtM3T6YMR4fk0u229FUlMd5E7rwQw')


@bot.message_handler(commands=['start'])
def start(message):
    photo = open('robo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, "Привет! Я бот, который умеет искать фильмы!")

    markup_inline = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    info = types.InlineKeyboardButton(text='помощь', callback_data='info')
    markup_inline.add(yes, no, info)
    bot.send_message(message.chat.id, 'Начать поиск?', reply_markup=markup_inline)


@bot.message_handler(commands=["список"])
def send_dock(message):
    dock = open('new_films.csv', 'rb')
    bot.send_document(message.chat.id, dock)


@bot.message_handler(commands=["Робо"])
def send_dock(message):
    p = open('robo.jpg', 'rb')
    bot.send_photo(message.chat.id, p)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Отлично! Поехали!')
        bot.send_message(call.from_user.id, films_for_today[0])
        random.shuffle(films_for_today)

        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        i_next = types.KeyboardButton('Другой')
        i_exit = types.KeyboardButton("Выход")
        markup_reply.add(i_next, i_exit)
        bot.send_message(call.message.chat.id, 'Посмотреть другой?', reply_markup=markup_reply)
    elif call.data == 'no':
        n = random.choice(num)
        bot.send_message(call.from_user.id, parting[n])
    elif call.data == 'info':
        bot.send_message(call.from_user.id,
                         'Для того, чтобы начать поиск, наберите /start. Для выхода нажмите на кнопку "Выход". Для продолжения поиска напишите в чате "Продолжить". ')
        bot.send_message(call.from_user.id, 'Если хотите поменять фильм нажмите "Другой".')
        photo0 = open('robo3.jpg', 'rb')
        bot.send_photo(call.from_user.id, photo0)
        bot.send_message(call.from_user.id, "Приятного поиска!")


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, "Вот что можно посмотреть сегодня:")
        bot.send_message(message.from_user.id, films_for_today[0])
        random.shuffle(films_for_today)

    elif message.text.lower() == 'другой' or message.text.lower() == 'продолжить':
        bot.send_message(message.from_user.id, films_for_today[0])
        random.shuffle(films_for_today)

    elif message.text.lower() == 'нет' or message.text.lower() == 'выход':
        n = random.choice(num)
        bot.send_message(message.from_user.id, parting[n])
    elif message.text == '/help':
        bot.send_message(message.from_user.id,
                         'Для того, чтобы начать поиск, наберите /start. Для выхода нажмите на кнопку "Выход". Для продолжения поиска напишите в чате "Продолжить". ')
        bot.send_message(message.from_user.id, 'Если хотите поменять фильм нажмите "Другой".')
        photo1 = open('robo2.jpg', 'rb')
        bot.send_photo(message.chat.id, photo1)
        bot.send_message(message.from_user.id, "Приятного поиска!")
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю, набери /help.')


def main():
    bot.polling(none_stop=True, interval=0)


films_info = s.get_info()
# запись в файл в формате csv
get_notes(films_info)

if __name__ == '__main__':
    main()
