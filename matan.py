import random

#Вопрос : Правильный ответ для вопроса.
question_dict = {"Аксиома полноты (или принцип полноты) для вещественных чисел формулируется так:"
                 "\n\n1) ∀ непустых X,Y ⊂ R: (X ≤ Y) => (∃ c ∈ R: X ≤ {c} ≤ Y)\n"
                 "2) ∀ непустых X, Y ⊂ R: (X ⊆ Y) => (∃ c ∈ R: X ∩ Y = {c})\n"
                 "3) ∀ пустых X, Y ⊂ R: (X ≤ Y) => (∃ c ∈ R: c ∉ X и c ∉ Y)\n"
                 "4) ∀ непустых X, Y ⊂ R: (X < Y) => (∃ c ∈ R: X < c < Y)" : '1',
                 "Определение супремума множества X\n\n"
                 "1) sup(X)=minUx,где Ux={y∈R:X≤y}\n"
                 "2) sup(X)=maxUx,где Ux={y∈R:X≥y}\n"
                 "3) sup(X)=minUx,где Ux={y∈R:y∈X}\n"
                 "4) sup(X)=maxUx,где Ux={y∈R:y<X}" : '1',
                 "Определение инфимума множества X\n\n"
                 "1) inf(X) = min Lx, где Lx = {y∈R:y≥X}\n"
                 "2) inf(X) = max Lx, где Lx = {y∈R:y>X}\n"
                 "3) inf(X) = min Lx, где Lx = {y∈R:y<X}\n"
                 "4) inf(X) = maxLx, где Lx​={y∈R:y≤X}" : '4',
                 "Сформулируй принцип Архимеда\n\n"
                 "1) ∀ ε > 0 ∀ x ∈ ℝ ∃ n ∈ ℕ : x > n · ε\n" 
                 "2) ∀ ε > 0 ∀ x ∈ ℝ ∃ n ∈ ℕ : n · ε < x\n"
                 "3) ∀ ε > 0 ∀ x ∈ ℝ ∃ n ∈ ℕ : x < n · ε\n"
                 "4) ∀ ε > 0 ∀ x ∈ ℝ ∃ n ∈ ℕ : x = n · ε\n" : '3'}

#Функция берет рандомный ключ, бот выводит ключ (вопрос) на экран. /
# return значение этого ключа (значение == правильный ответ)

def question_func(question_d):
    question = random.choice(list(question_d.keys()))
    answer = question_d.get(question)
    return question, answer


