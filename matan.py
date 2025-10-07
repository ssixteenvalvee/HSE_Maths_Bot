import random

#Вопрос : Правильный ответ для вопроса.
question_dict = {"Какой-то вопрос?\n1.Ответ 1\t\t2.Ответ 2\n3.Answer 3\t\t4.Answer 4" : '3',
                 "Тоже важный математический вопрос?\n1.Answer 1\t\t2.Answer 2" : '2'}

#Функция берет рандомный ключ, бот выводит ключ (вопрос) на экран. /
# return значение этого ключа (значение == правильный ответ)

def question_func(question_d):
    question = random.choice(list(question_d.keys()))
    answer = question_d.get(question)
    return question, answer


