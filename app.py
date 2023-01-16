
import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> ' \
           ' <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nУвидеть список всех доступных валют:/values'
    bot.reply_to(message, f"Hi, {message.chat.username}!\n{text}")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException(f'Ожидается 3 аргумента, получено {len(values)}')
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать коанду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount):.2f}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
