import telebot 
from telebot import types
from bs4 import BeautifulSoup
import requests

# создаем бота с токеном
bot = telebot.TeleBot('ваш токен')

# функция для парсинга сайта
def parse_events(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    events = soup.find_all('div', class_='impression-card')

    events_list = []
    for event in events:
        event_title = event.find('a', class_='impression-card-title').text.strip()
        event_info = event.find('div', class_='impression-card-info').text.strip()
        events_list.append(f'<b>{event_title}</b>\nПодробная информация: {event_info}\n ')
    return '\n\n'.join(events_list)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Билеты")
btn2 = types.KeyboardButton("Афиша")
btn3 = types.KeyboardButton("Места")
markup.add(btn1, btn2, btn3)

# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEH7ydj_dPP25K24ak5pzROOfsNcLH3LQAC3iYAAjyzoEv9zZO47HGC7y4E')
    
    bot.reply_to(message, 
    f'Привет {message.chat.first_name}! Я помогу тебе узнать о событиях в Астане. Выбери категорию, которая тебя интересует: ', 
    reply_markup=markup)
    bot.send_message(message.chat.id, 'Если бот не отвечает сообщите сюда -> @Aske_xa')

# обрабатываем команду /events
@bot.message_handler(content_types=['text'])
def send_events(message):
    if(message.text == "Билеты"):
        events = parse_events('https://sxodim.com/astana/tickets')
        bot.send_message(message.chat.id, events, parse_mode='HTML')
        bot.send_message(message.chat.id, 'Подробная инфрмация на сайте https://sxodim.com/astana/tickets', parse_mode='HTML', reply_markup=markup)
    elif(message.text == "Афиша"):
        events = parse_events('https://sxodim.com/astana/afisha')
        bot.send_message(message.chat.id, events, parse_mode='HTML')
        bot.send_message(message.chat.id, 'Подробная инфрмация на сайте https://sxodim.com/astana/afisha', parse_mode='HTML', reply_markup=markup)
    elif(message.text == "Места"):
        events = parse_events('https://sxodim.com/astana/places')
        bot.send_message(message.chat.id, events, parse_mode='HTML')
        bot.send_message(message.chat.id, 'Подробная инфрмация на сайте https://sxodim.com/astana/places', parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю')
        bot.send_message(message.chat.id, 'Выберите категорию')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEH7ylj_dQFjHKtWuc_Nj9mIxa4G4rB3AACNikAAnLlmEs4N8YGTxR7ni4E')

# запускаем бота
bot.polling()


