from telebot import *
from TelegramBotAPI import *
from random import *

hicomms = ['Hi There!', 'Hello!', "Good to see you!"]

bot = telebot.TeleBot(token='8419048956:AAFqhlf9jTcbmFQZNbA1DG8Mqdk-1afiqp4')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'{choice(hicomms)} Хочешь проверить свои математические навыки?')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Конечно!")
    markup.add(btn1)
    bot.send_message(message.chat.id, text='', reply_markup=markup)

@bot.message_handler()
def ask_subject(message):
    if (message.text) == "Конечно!":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Математический Анализ")
        btn2 = types.KeyboardButton("Линейная алгебра")
        btn3 = types.KeyboardButton("Дискретная Математика")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Итак, {0.first_name}, какой предмет нужно вспомнить?".format(
                         message.from_user), reply_markup=markup)

bot.infinity_polling()
