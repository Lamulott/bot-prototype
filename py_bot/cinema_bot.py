import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as b
import random


URL = 'https://www.baskino.re/novinki-v2/'
def parser(url) -> list[str]:
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    films = soup.find('div', class_ ='shortpost')
    total_list = []
    for films in soup.find_all('div', class_ ='shortpost'):
        link = films.div.a['href']
        name = films.div.a.img['title']
        total_list.append(f'{name} {link}')
    return total_list

films_for_today = parser(URL)
random.shuffle(films_for_today)

parting = ['До новых встреч!', 'До встречи!', 'Пока-пока!', 'До скорой встречи!', 'До следующей встречи!', 'See you soon!']
random.shuffle(parting)
num = [i for i in range(len(parting))]

bot = telebot.TeleBot('6918194595:AAHo7WOtM3T6YMR4fk0u229FUlMd5E7rwQw')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id,
                   photo='https://cdn.dribbble.com/users/1436489/screenshots/4653126/bot_bruxelles_loop.gif')
    bot.send_message(message.chat.id, "Привет! Я бот, который ищет фильмы. Начать поиск?")
    bot.send_message(message.chat.id, 'Введите Да/Нет')

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Отлично! Поехали!')
        bot.send_message(message.from_user.id, "Вот что можно посмотреть сегодня:")
        bot.send_message(message.from_user.id, films_for_today[0])

    elif message.text.lower() == 'другой':
        bot.send_message(message.from_user.id, films_for_today[0])
        del films_for_today[0]

    elif message.text.lower() == 'нет' or message.text.lower() == 'выход':
        n = random.choice(num)
        bot.send_message(message.from_user.id, parting[n])
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Если Вы хотите продолжить поиск, наберите  "Дa". Для выхода введите "Нет". Если Вы хотите выбрать другой фильм, напишите "другой"')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю, набери /help.')



# обработчик нажатой кнопки
@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.data == 'url':
        msg = 'К сожалению пока этот бот находится на стадии разработки'
        # отправляем в тг
        bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)