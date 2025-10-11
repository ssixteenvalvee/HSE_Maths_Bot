from telebot import *
from random import *

bot = telebot.TeleBot(token='8419048956:AAFqhlf9jTcbmFQZNbA1DG8Mqdk-1afiqp4')

# Различные сообщения
hi_comments = ['Привет!', 'Доброго времени суток,', "Рад тебя видеть!"]
matan_comments = ['Приступим.', 'Вперёд!', 'Постигнем же Математический Анализ!']
linal_comments = ['Узнаем же азы Линейной Алгебры!', 'Вперёд!']
different_comments = ['Давай начнём.', 'Отлично, вперёд!']

# Появление кнопок выбора предмета
def buttons_appear(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_matan = types.KeyboardButton("Математический Анализ")
    btn_linal = types.KeyboardButton("Линейная Алгебра")
    btn_diskretka = types.KeyboardButton("Дискретная Математика")
    markup.add(btn_matan, btn_linal, btn_diskretka)
    bot.send_message(message.chat.id, text="Итак, {0.first_name}, какой предмет нужно вспомнить?".format(
        message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, where_to_go)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Конечно!")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=f'{choice(hi_comments)}\nХочешь проверить свои математические навыки?', reply_markup=markup)

# Обработка команды /recover
@bot.message_handler(commands=['recover'])
def recover_kbd(message):
    keyboard_remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text='Возвращаемся в начало...', reply_markup=keyboard_remove)
    print(f'chat_id: {message.chat.id} has been recovered...\n')
    buttons_appear(message)

# Обработка сообщений пользователя
@bot.message_handler()
def ask_subject(message):
    if message.text == "Конечно!":
        buttons_appear(message)

def return_to_the_menu(message):
    if message.text == "В главное меню!":
        recover_kbd(message)

def where_to_go(message):
    keyboard_remove = types.ReplyKeyboardRemove()
    if message.text == "Математический Анализ":
        bot.send_message(message.chat.id, text= f'{choice(matan_comments)}', reply_markup=keyboard_remove)
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
        ask_matan(message)
    elif message.text == "Линейная Алгебра":
        bot.send_message(message.chat.id, text= f'{choice(linal_comments)}', reply_markup=keyboard_remove)
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_linal)
        ask_linal(message)
    elif message.text == "Дискретная Математика":
        bot.send_message(message.chat.id, text=f'{choice(different_comments)}', reply_markup=keyboard_remove)
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_diskretka)
        ask_diskretka(message)

def is_it_right(true_answer, student_answer):
    if true_answer == student_answer:
        return True
    return False

# Математический анализ
@bot.message_handler()
def ask_matan(message):
    if message.text == "Математический Анализ" or message.text == "Следующий вопрос!":
        from matan import question_dict, question_func
        question, true_answer = question_func(question_dict)  # def return question, answer (look matan.py)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID is {message.chat.id} The question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, true_answer)
    else: return_to_the_menu(message)

def answer_matan(message, true_answer):
    if message.text != "Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('Следующий вопрос!')
            btn_recover = types.KeyboardButton('В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
            print(f'Correct. Chat_ID is {message.chat.id}\n')
        else:
            bot.send_message(message.chat.id, text=f"Неверно! Попробуй ещё.")
            print(f'Incorrect. Chat_ID is {message.chat.id}')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, true_answer)
    else:
        recover_kbd(message)

# Линейная Алгебра
@bot.message_handler()
def ask_linal(message):
    if message.text == "Линейная Алгебра" or message.text == "Следующий вопрос!!":
        from linal import question_dict, question_func
        question, true_answer = question_func(question_dict)  # def return question, answer (look matan.py)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID is {message.chat.id} The question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_linal, true_answer)
    else: return_to_the_menu(message)

def answer_linal(message, true_answer):
    if message.text != "Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('Следующий вопрос!!')
            btn_recover = types.KeyboardButton('В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_linal)
            print(f'Correct. Chat_ID is {message.chat.id}\n')
        else:
            bot.send_message(message.chat.id, text=f"Неверно! Попробуй ещё.")
            print(f'Incorrect. Chat_ID is {message.chat.id}')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_linal, true_answer)
    else:
        recover_kbd(message)

# Дискретная Математика
@bot.message_handler()
def ask_diskretka(message):
    if message.text == "Дискретная Математика" or message.text == "Слeдующий вопрос!":
        from diskretka import question_dict, question_func
        question, true_answer = question_func(question_dict)  # def return question, answer (look matan.py)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID is {message.chat.id} The question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_diskretka, true_answer)
    else: return_to_the_menu(message)

def answer_diskretka(message, true_answer):
    if message.text != "Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('Слeдующий вопрос!')
            btn_recover = types.KeyboardButton('В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_diskretka)
            print(f'Correct. Chat_ID is {message.chat.id}\n')
        else:
            bot.send_message(message.chat.id, text=f"Неверно! Попробуй ещё.")
            print(f'Incorrect. Chat_ID is {message.chat.id}')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_diskretka, true_answer)
    else:
        recover_kbd(message)

bot.infinity_polling()
