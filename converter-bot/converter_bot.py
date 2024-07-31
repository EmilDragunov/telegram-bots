import telebot
from currency_converter import CurrencyConverter
from telebot import types
from config import YOUR_TOKEN


bot = telebot.TeleBot(YOUR_TOKEN)
currency = CurrencyConverter
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
        btn2 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
        btn3 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
        btn4 = types.InlineKeyboardButton('USD/CNY', callback_data='USD/CNY')
        btn5 = types.InlineKeyboardButton('USD/GBP', callback_data='USD/GBP')
        btn6 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0, впишите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.split('/')
        res = currency().convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через /")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency().convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то не так, впишите значение заново')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)
