import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, CyrrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Введите сообщение в виде <имя валюты, цену которой он хочет узнать> \
<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nУвидеть список доступных валют /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        value = message.text.split(' ')
        if len(value)!=3:
            raise ConvertionExeption('Слишко много пораметров')

        quote, base, amount = value
        total_base = CyrrencyConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} {total_base} '
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
