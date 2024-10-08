import random


def switch_case_set(set):
    if set == 1:
        return "зниження ваги"
    elif set == 2:
        return "підтримки ваги"
    elif set == 3:
        return "набору ваги"
    else:
        raise ValueError("Помилка з обраним сетом тренувань...")


weight = float(input("Введіть вагу: "))                    # User enters weight
height = float(input("Введіть ріст в см: ")) / 100        # User enters height

if not (0 <= height < 3 and 0 <= weight <= 300):           # Checking the correctness of variables
    raise ValueError(
        "Будь ласка, введіть реалістичні значення зросту та ваги.")

bmi_value = weight / (height ** 2)                         # Calculation of BMI
print(bmi_value)                                            # Derivation of BMI

if bmi_value < 18.5:                                        # Analysis of BMI
    # Random recommendations for underweight
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

# пропонуємо користувачу вибрати сет тренувань для: скидання/підтримування/набір ваги
if bmi_value < 18.5:
    print("За результатами ІМТ ми пропонуємо сет тренувань для «набору ваги»")
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

print(f"Ви обрали cет тренувань для {switch_case_set(set)}")
