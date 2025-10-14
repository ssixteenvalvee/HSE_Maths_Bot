from multiprocessing.resource_tracker import register

from telebot import *
from random import *

bot = telebot.TeleBot(token='8419048956:AAFqhlf9jTcbmFQZNbA1DG8Mqdk-1afiqp4')

# Различные сообщения
hi_comments = ['Привет!', 'Доброго времени суток,', "Рад тебя видеть!"]
matan_comments = ['Приступим.', 'Вперёд!', 'Постигнем же Математический Анализ!']
linal_comments = ['Узнаем же азы Линейной Алгебры!', 'Вперёд!']
different_comments = ['Давай начнём.', 'Отлично, вперёд!']
you_are_stupid_comments = ['У вас небольшие трудности с этой темой, советуем её повторить.', 'Ошибки - лучшие учителя!']

prev_questions_list = [] # !
incorrect_questions_list = [] # !

# Появление кнопок выбора предмета
def buttons_appear(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_matan = types.KeyboardButton("📊 Математический Анализ")
    btn_linal = types.KeyboardButton("📐 Линейная Алгебра")
    btn_diskretka = types.KeyboardButton("🔢 Дискретная Математика")
    markup.row(btn_matan)
    markup.row(btn_linal)
    markup.row(btn_diskretka)
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
    print(f'Chat_ID: {message.chat.id}, name: {message.chat.first_name} pressed /recover...\n')
    buttons_appear(message)

# Обработка сообщений пользователя
@bot.message_handler()
def ask_subject(message):
    if message.text == "Конечно!":
        buttons_appear(message)

def return_to_the_menu(message):
    if message.text == "⬅️ В главное меню!":
        recover_kbd(message)

def where_to_go(message):
    keyboard_remove = types.ReplyKeyboardRemove()
    if message.text == "📊 Математический Анализ":
        bot.send_message(message.chat.id, text= f'{choice(matan_comments)}', reply_markup=keyboard_remove)
        #bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
        ask_matan(message)
    elif message.text == "📐 Линейная Алгебра":
        bot.send_message(message.chat.id, text= f'{choice(linal_comments)}', reply_markup=keyboard_remove)
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_linal)
        ask_linal(message)
    elif message.text == "🔢 Дискретная Математика":
        bot.send_message(message.chat.id, text=f'{choice(different_comments)}', reply_markup=keyboard_remove)
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_diskretka)
        ask_diskretka(message)

def is_it_right(true_answer, student_answer):
    if true_answer == student_answer:
        return True
    return False

# mistakes block
def no_more(message):
    print(incorrect_questions_list, sep='\n')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btny = types.KeyboardButton("Да.")
    btnn = types.KeyboardButton("Нет.")
    markup.add(btny, btnn)
    bot.send_message(message.chat.id, text='Это были все вопросы.\n\nЖелаете исправить ошибки?', reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(message.chat.id, ask_mistakes)

def ask_mistakes(message):
    if message.text == 'Следующая Ошибка' or message.text == 'Да.':
        if len(incorrect_questions_list) > 0:
            questionm = incorrect_questions_list.pop(0)
            correct_ans = incorrect_questions_list.pop(0)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
            btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
            btn_close = types.KeyboardButton('Завершить работу над ошибками')
            markup.add(btn1, btn2, btn3, btn4, btn_close)
            bot.send_message(message.chat.id, text=f'{questionm}', reply_markup=markup)
            print(f'MISTAKES PART || {questionm}, name: {message.chat.first_name} chat_ID {message.chat.id}\n')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_mistakes, correct_ans)
        else:
            bot.send_message(message.chat.id, text='Вы закончили работу над ошибками. Так держать!')
            recover_kbd(message)
    else:
        recover_kbd(message)

def answer_mistakes(message, correct_ans):
    if message.text != "Завершить работу над ошибками":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_continue = types.KeyboardButton('Следующая Ошибка')
        btn_recover = types.KeyboardButton('⬅️ В главное меню')
        markup.add(btn_continue)
        markup.add(btn_recover)
        if is_it_right(correct_ans, message.text) is True:
            bot.send_message(message.chat.id, text=f"✅ Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_mistakes)
            print(f'MISTAKES PART || Correct. Chat_ID: {message.chat.id}, name: {message.chat.first_name}\n')
        else:
            bot.send_message(message.chat.id, text=f'{choice(you_are_stupid_comments)}')
            bot.register_next_step_handler_by_chat_id(message.chat.id, answer_mistakes, correct_ans)
    else:
        recover_kbd(message)

# Математический анализ
from matan import question_dict_matan, question_func
func_dict_matan = dict()
@bot.message_handler()
def ask_matan(message):
    print('ask_matan_part')
    global func_dict_matan
    if message.text == "📊 Математический Анализ" or message.text == "➡️ Следующий вопрос!":
        if message.text == "📊 Математический Анализ":
            func_dict_matan = dict.copy(question_dict_matan)
        if len(func_dict_matan) == 0:
            print(func_dict_matan.keys(), sep='\n')
            no_more(message)
        question, true_answer, q_amount = question_func(func_dict_matan)  # def return question, answer, quest. amount (look matan.py)
        print(question, true_answer, q_amount, 'func dict output')
        del func_dict_matan[question]
        print(question_dict_matan, sep='\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('⬅️ Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID: {message.chat.id}, name: {message.chat.first_name}\nThe question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, true_answer, question)
    else: return_to_the_menu(message)

def answer_matan(message, true_answer, question):
    print(f'\nanswer_matan part')
    if message.text != "⬅️ Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Следующий вопрос!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"✅ Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
            print(f'Correct. Chat_ID: {message.chat.id}, name: {message.chat.first_name}\n')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Следующий вопрос!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Неверно! Вы сможете вернуться к вопросу позже.", reply_markup=markup)
            incorrect_questions_list.append(question)
            incorrect_questions_list.append(true_answer)
            print(f'incorrect_questions_list: {incorrect_questions_list}')
            print(f'Incorrect. Chat_ID: {message.chat.id}, name: {message.chat.first_name}')
            #bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, true_answer, question)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_matan)
    else:
        recover_kbd(message)

# Линейная Алгебра
from linal import question_dict_linal, question_func
func_dict_linal = dict()
@bot.message_handler()
def ask_linal(message):
    print('\nask_linal_part\n')
    global func_dict_linal
    if message.text == "📐 Линейная Алгебра" or message.text == "➡️ Следующий вопрос!!":
        if message.text == "📐 Линейная Алгебра":
            func_dict_linal = dict.copy(question_dict_linal)
        if len(func_dict_linal) == 0:
            print(func_dict_linal.keys(), sep='\n')
            no_more(message)
        question, true_answer, q_amount = question_func(func_dict_linal)  # def return question, answer, quest. amount (look linal.py)
        print(question, true_answer, q_amount, 'func dict output')
        del func_dict_linal[question]
        print(question_dict_linal, sep='\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('⬅️ Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID: {message.chat.id}, name: {message.chat.first_name}\nThe question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_linal, true_answer, question)
    else: return_to_the_menu(message)

def answer_linal(message, true_answer, question):
    print(f'\nanswer_linal part\n')
    if message.text != "⬅️ Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Следующий вопрос!!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"✅ Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_linal)
            print(f'Correct. Chat_ID: {message.chat.id}, name: {message.chat.first_name}\n')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Следующий вопрос!!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Неверно! Вы сможете вернуться к вопросу позже.", reply_markup=markup)
            incorrect_questions_list.append(question)
            incorrect_questions_list.append(true_answer)
            print(f'incorrect_questions_list: {incorrect_questions_list}')
            print(f'Incorrect. Chat_ID: {message.chat.id}, name: {message.chat.first_name}')
            #bot.register_next_step_handler_by_chat_id(message.chat.id, answer_matan, true_answer, question)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_linal)
    else:
        recover_kbd(message)

# Дискретная Математика
from diskretka import question_dict_diskretka, question_func
func_dict_diskretka = dict()
@bot.message_handler()
def ask_diskretka(message):
    print('\nask_diskretka_part\n')
    global func_dict_diskretka
    if message.text == "🔢 Дискретная Математика" or message.text == "➡️ Слeдующий вопрос!":
        if message.text == "🔢 Дискретная Математика":
            func_dict_diskretka = dict.copy(question_dict_diskretka)
        if len(func_dict_diskretka) == 0:
            print(func_dict_diskretka.keys(), sep='\n')
            no_more(message)
        question, true_answer, q_amount = question_func(func_dict_diskretka)  # def return question, answer, quest. amount (look diskretka.py)
        print(question, true_answer, q_amount, 'func dict output')
        del func_dict_diskretka[question]
        print(question_dict_diskretka, sep='\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1, btn2 = types.KeyboardButton('1'), types.KeyboardButton('2')
        btn3, btn4 = types.KeyboardButton('3'), types.KeyboardButton('4')
        btn_close = types.KeyboardButton('⬅️ Завершить тестирование')
        markup.add(btn1, btn2, btn3, btn4, btn_close)
        bot.send_message(message.chat.id, text=f'{question}', reply_markup=markup)
        print(f'Chat_ID: {message.chat.id}, name: {message.chat.first_name}\nThe question is {question}')
        bot.register_next_step_handler_by_chat_id(message.chat.id, answer_diskretka, true_answer, question)
    else: return_to_the_menu(message)

def answer_diskretka(message, true_answer, question):
    print(f'\nanswer_diskretka part')
    if message.text != "⬅️ Завершить тестирование":
        if is_it_right(true_answer, message.text) is True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Слeдующий вопрос!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"✅ Это верно!", reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_diskretka)
            print(f'Correct. Chat_ID: {message.chat.id}, name: {message.chat.first_name}\n')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_continue = types.KeyboardButton('➡️ Слeдующий вопрос!')
            btn_recover = types.KeyboardButton('⬅️ В главное меню!')
            markup.add(btn_continue)
            markup.add(btn_recover)
            bot.send_message(message.chat.id, text=f"Неверно! Вы сможете вернуться к вопросу позже.", reply_markup=markup)
            incorrect_questions_list.append(question)
            incorrect_questions_list.append(true_answer)
            print(f'incorrect_questions_list: {incorrect_questions_list}')
            print(f'Incorrect. Chat_ID: {message.chat.id}, name: {message.chat.first_name}')
            #bot.register_next_step_handler_by_chat_id(message.chat.id, answer_diskretka, true_answer, question)
            bot.register_next_step_handler_by_chat_id(message.chat.id, ask_diskretka)
    else:
        recover_kbd(message)

bot.infinity_polling()
