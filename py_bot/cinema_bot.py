import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as b
import random

# url_list = ['https://www.baskino.re/novinki-v2/', 'https://baskino.re/novinki-v2/page/2/']
url = 'https://www.baskino.re/novinki-v2/'
headers = {
    'Accept': '*/*',
    'User_Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.731 Mobile Safari/537.36'
}

def parser(url, headers) -> list[str]:
    r = requests.get(url, headers=headers)
    soup = b(r.text, 'html.parser')
    films = soup.find('div', class_='shortpost')
    total_list = []
    for films in soup.find_all('div', class_='shortpost'):
        link = films.div.a['href']
        name = films.div.a.img['title']
        total_list.append(f'{name} {link}')
    return total_list


films_for_today = parser(url, headers)
random.shuffle(films_for_today)

parting = ['До новых встреч!', 'До встречи!', 'Пока-пока!', 'До скорой встречи!', 'До следующей встречи!',
           'See you soon!']
random.shuffle(parting)
num = [i for i in range(len(parting))]

bot = telebot.TeleBot('6918194595:AAHo7WOtM3T6YMR4fk0u229FUlMd5E7rwQw')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id,
                   photo='https://cdn.dribbble.com/users/1436489/screenshots/4653126/bot_bruxelles_loop.gif')
    bot.send_message(message.chat.id, "Привет! Я бот, который ищет фильмы.")

    markup_inline = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    info = types.InlineKeyboardButton(text='помощь', callback_data='info')
    markup_inline.add(yes, no, info)
    bot.send_message(message.chat.id, 'Хотите начать поиск?', reply_markup=markup_inline)


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
        bot.send_message(call.message.chat.id, 'Посмотреть что-нибудь другое?', reply_markup=markup_reply)
    elif call.data == 'no':
        n = random.choice(num)
        bot.send_message(call.from_user.id, parting[n])
    elif call.data == 'info':
        bot.send_message(call.from_user.id,
                         'Для того, чтобы начать поиск, нажмите "Дa". Для выхода нажмите "Нет" или "Выход". Для выбора другого фильма нажмите кнопку "другой". Так же для продолжения поиска Вы можете набрать в чате "Начать". Приятного поиска!')


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, "Вот что можно посмотреть сегодня:")
        bot.send_message(message.from_user.id, films_for_today[0])

    elif message.text.lower() == 'другой' or message.text.lower() == 'начать':
        bot.send_message(message.from_user.id, films_for_today[0])
        del films_for_today[0]

    elif message.text.lower() == 'нет' or message.text.lower() == 'выход':
        n = random.choice(num)
        bot.send_message(message.from_user.id, parting[n])
    elif message.text == '/help':
        bot.send_message(message.from_user.id,
                         'Для того, чтобы начать поиск, нажмите "Дa". Для выхода нажмите "Нет" или "Выход". Для выбора другого фильма нажмите кнопку "другой". Так же для продолжения поиска Вы можете набрать в чате "Начать". Приятного поиска!')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю, набери /help.')


# обработчик нажатой кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'url':
        msg = 'К сожалению пока этот бот находится на стадии разработки'
        # отправляем в тг
        bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
