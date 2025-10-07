from telebot import *
from TelegramBotAPI import *
from random import *

hicomms = ['Привет!', 'Доброго времени суток,', "Рад вас видеть!"]

bot = telebot.TeleBot(token='token')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Конечно!")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=f'{choice(hicomms)} Хочешь проверить свои математические навыки?', reply_markup=markup)

@bot.message_handler(commands=['recover'])
def recover_kbd(message):
    kbrd_remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=kbrd_remove)

@bot.message_handler()
def ask_subject(message):
    if (message.text) == "Конечно!":
        kbrd_remove = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text='Отлично!', reply_markup=kbrd_remove)
        btnm = types.KeyboardButton("Математический Анализ")
        btnl = types.KeyboardButton("Линейная алгебра")
        btnd = types.KeyboardButton("Дискретная Математика")
        markup.add(btnm, btnl, btnd)
        bot.send_message(message.chat.id, text="Итак, {0.first_name}, какой предмет нужно вспомнить?".format(
                         message.from_user), reply_markup=markup)

bot.infinity_polling()
