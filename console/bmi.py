import random


def weight_in():            # User enters weight
    # wght = input("Введіть вагу: ")
    while True:
        try:
            wght = input("Введіть вагу: ")
            try:
                weight = float(wght)
                return weight
            except ValueError:
                print("Було введено не коректну вагу! ще раз <<")
                raise
            break
        except ValueError:
            print("Помилку було оброблено")

    '''if wght.isdigit():
        return float(wght)
    else:
        raise ValueError(
            "\t>> Було введено не коректну вагу! Вагу потрібно вводити цифрами <<")'''


def heiіght_in():            # User enters height
    hght = input("Введіть ріст в см: ")
    if hght.isdigit():
        return float(hght)/100
    else:
        raise ValueError(
            "\t>> Було введено не коректний ріст! Ріст потрібно вводити цифрами <<")


# Checking the correctness of variables
def check_correct_variables(wght, hght):
    if not (0 <= hght < 3 and 0 <= wght <= 300):
        raise ValueError(
            "Будь ласка, введіть реалістичні значення зросту чи ваги.")


def bmi_calculation(wght, hght):            # Calculation of BMI
    return wght / (hght ** 2)


def switch_case_set(set):
    if set == 1:
        return "зниження ваги"
    elif set == 2:
        return "підтримки ваги"
    elif set == 3:
        return "набору ваги"
    else:
        raise ValueError("Помилка з обраним сетом тренувань...")


weight = weight_in()
height = height_in()

check_correct_variables(weight, height)

bmi_value = bmi_calculation(weight, height)

print(bmi_value)                                            # Derivation of BMI

# Analysis of BMI# Random recommendations for underweight
if bmi_value < 18.5:
    recommendations_underweight = [
        "Ваш ІМТ є нижчим норми. Перед початком тренувань рекомендуємо звернутися до спеціаліста. Ви можете обрати план тренувань «набір ваги» і вводити у раціон більшу кількість калорій.",
        "Ваш ІМТ є заниженим. Перед початком тренувань рекомендуємо звернутися до спеціаліста для індивідуальної консультації.",
        "Ваш ІМТ є нижчим від норми. Рекомендуємо звернутися до спеціаліста для індивідуальної консультації."
    ]
    print(random.choice(recommendations_underweight))
elif bmi_value >= 18.5 and bmi_value < 24.9:               # Random recommendations for normal weight
    recommendations_normal = [
        "Вітаємо, у вас ІМТ в межах норми. Ми рекомендуємо обрати наш план тренувань «підтримка ваги».",
        "Ваш ІМТ в нормі. Рекомендуємо план «підтримка ваги» для підтримки вашого стану.",
        "Вітаємо, у вас нормальний ІМТ. Ми рекомендуємо план тренувань «підтримка ваги»."
    ]
    print(random.choice(recommendations_normal))
elif bmi_value >= 25 and bmi_value < 29.9:                  # Recommendations for overweight
    recommendations_overweight = [
        "Ваш ІМТ є завищеним, рекомендуємо план тренувань «зниження ваги».",
        "Ваш ІМТ трохи перевищує норму. Рекомендуємо вам план тренувань «зниження ваги».",
        "Ваш ІМТ є трохи завищеним. Рекомендуємо вам план тренувань «зниження ваги»."
    ]
    print(random.choice(recommendations_overweight))
else:
    recommendations_obesity = [
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо звернутись до спеціаліста та обрати план «зниження ваги».",
        "У вас ІМТ, що вказує на ожиріння. Рекомендуємо обрати план тренувань «зниження ваги».",
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо консультацію з дієтологом і план «зниження ваги»."
    ]
    print(random.choice(recommendations_obesity))

if bmi_value < 18.5:            # пропонуємо користувачу вибрати сет тренувань для: скидання/підтримування/набір ваги
    print("За результатами ІМТ вам доступний сет тренувань для «набору ваги»")
    set = 3
elif bmi_value >= 18.5 and bmi_value < 24.9:
    print("За результатами ІМТ ми пропонуємо сет тренувань для «зниження ваги» «підтримки ваги» «набору ваги»")
    set = int(input("Виберіть що вас цікавить(зниження-1 підтримка-2 набір-3): "))
    if not (set == 1 or set == 2 or set == 3):           # Checking the correctness of variables
        raise ValueError("Ви ввели не коректну команду...")
else:
    print("За результатами ІМТ ми пропонуємо сет тренувань для «зниження ваги» або «підтримки ваги» ")
    set = int(input("Виберіть що вас цікавить(зниження-1 підтримка-2): "))
    if not (set == 1 or set == 2):           # Checking the correctness of variables
        raise ValueError("Ви ввели не коректну команду...")

print(f"Сет тренувань для {switch_case_set(set)}")

# frequency
