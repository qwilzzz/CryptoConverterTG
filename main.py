import telebot

from config import token, keys
from extensions import APIException, Converter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def hello(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Список доступных валют можно узнать командой /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = (f'Цена {amount} {quote} в {base} - {total_base}')
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)