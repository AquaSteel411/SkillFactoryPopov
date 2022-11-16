'''
Использован европейский сервис по определению курса валют - https://www.currate.ru/
Данные курсов валют отличаются от ЦБ РФ.
'''

import telebot

from extensions import APIException, Converter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


# Обоработчик основной информации о работе с ботом
@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    info = '''
    Для начала работы с ботом, введите команду в следующем формате через пробел:
<имя валюты, цену которой вы хочете узнать> 
<имя валюты, в которой надо узнать цену первой валюты> 
<количество первой валюты>
Чтобы узнать список доступных валют введите: /value
'''
    bot.reply_to(message, info)


# Обработчик показывающий доступные валюты
@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# Основной обработчик конвертора
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    # Добавляем кнопки /help и /value для удобства пользователя
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    item1 = telebot.types.KeyboardButton('/help')
    item2 = telebot.types.KeyboardButton('/value')
    markup.row(item1, item2)
    try:
        elem = message.text.lower().split()

        if len(elem) != 3:
            raise APIException('Неверное количество параметров!')

        base, quote, amount = elem
        total = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Неверный ввод!\n{e}', reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {base} = {total} {quote}'
        bot.reply_to(message, text, reply_markup=markup)


if __name__ == '__main__':
    bot.polling()
