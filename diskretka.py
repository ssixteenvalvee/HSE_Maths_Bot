import random

#Вопрос : Правильный ответ для вопроса.
question_dict = {"Вопрос:"
                 "\n\n1) \n"
                 "2) \n"
                 "3) \n"
                 "4) " : '3'
                 }

#Функция берет рандомный ключ, бот выводит ключ (вопрос) на экран. /
# return значение этого ключа (значение == правильный ответ)

def question_func(question_d):
    question = random.choice(list(question_d.keys()))
    answer = question_d.get(question)
    return question, answer