from multiprocessing.resource_tracker import register

from telebot import *
from TelegramBotAPI import *
from random import *

hicomms = ['Привет!', 'Доброго времени суток,', "Рад тебя видеть!"]
mtncomms = ['Видимо ты не смог доказать, что один больше нуля...']
comms = ['Давай начнём.', 'Отлично, вперёд!']

bot = telebot.TeleBot(token='8419048956:AAFqhlf9jTcbmFQZNbA1DG8Mqdk-1afiqp4')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Конечно!")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=f'{choice(hicomms)} Хочешь проверить свои математические навыки?', reply_markup=markup)

@bot.message_handler(commands=['recover'])
def recover_kbd(message):
    kbrd_remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text='Возвращаемся в начало...', reply_markup=kbrd_remove)
    print(f'chat_id: {message.chat.id} has been recovered...\n')

@bot.message_handler()
def ask_subject(message):
    if (message.text) == "Конечно!":
        kbrd_remove = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text='Отлично!', reply_markup=kbrd_remove)
        btnm = types.KeyboardButton("Математический Анализ")
        btnl = types.KeyboardButton("Линейная Алгебра")
        btnd = types.KeyboardButton("Дискретная Математика")
        markup.add(btnm, btnl, btnd)
        bot.send_message(message.chat.id, text="Итак, {0.first_name}, какой предмет нужно вспомнить?".format(
                         message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, where_to_go)

def where_to_go(message):
    kbrd_remove = types.ReplyKeyboardRemove()
    if (message.text) == "Математический Анализ":
        bot.send_message(message.chat.id, text= f'{choice(mtncomms)}', reply_markup=kbrd_remove)
        #bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
        ask_matan(message)
    if (message.text) == "Линейная алгебра":
        bot.send_message(message.chat.id, text= f'{choice(comms)}', reply_markup=kbrd_remove)
    if (message.text) == "Дискретная Математика":
        bot.send_message(message.chat.id, text=f'{choice(comms)}', reply_markup=kbrd_remove)

def is_it_right(trueans, stud_answer):
    if trueans == stud_answer:
        return True
    return False
@bot.message_handler()
def ask_matan(message):
    if message.text == "Математический Анализ" or message.text == "Следующий вопрос!":
        from matan import question_dict, question_func
        question, trueanswer = question_func(question_dict)  # def return question, answer (look matan.py)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btnclose = types.KeyboardButton('Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btnclose)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID is {message.chat.id} The question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, trueanswer)


def answer_matan(message, trueanswer):
    if message.text != "Завершить тестирование":
        if is_it_right(trueanswer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('Следующий вопрос!')
            markup.add(btn_continue)
            bot.send_message(message.chat.id, text=f"Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
            print(f'Correct. Chat_ID is {message.chat.id}\n')
        else:
            bot.send_message(message.chat.id, text=f"Неверно! Попробуй ещё.")
            print(f'Incorrect. Chat_ID is {message.chat.id}')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, trueanswer)
    else:
        recover_kbd(message)

bot.infinity_polling()
