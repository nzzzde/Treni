import random


def weight_in():                            # User enters weight
    while True:
        wght = input("Введіть вагу: ")
        try:
            weight = float(wght)
        except ValueError:
            print("Вагу потрібно вводити числом! \nСпробуйте ще раз.\n")
        else:
            try:
                if (15 <= weight <= 300):        # Checking the correctness of variables
                    return weight
                else:
                    raise ValueError(
                        f"{weight}кг не є реалістичною вагою людини")
            except ValueError as er_ror:
                print(f"{er_ror}\nСпробуйте ще раз.\n")


def height_in():                            # User enters height
    while True:
        hght = input("Введіть ріст в см: ")
        try:
            height = float(hght)/100
        except ValueError:
            print("Ріст потрібно вводити числом! \nСпробуйте ще раз.\n")
        else:
            try:
                if (0.3 <= height <= 3):        # Checking the correctness of variables
                    return height
                else:
                    raise ValueError(
                        f"{height}м не є реалістичним ростом людини")
            except ValueError as er_ror:
                print(f"{er_ror}\nСпробуйте ще раз.\n")


def bmi_calculation(wght, hght):            # Calculation of BMI
    return wght / (hght ** 2)


def choice_set(bmi):  # user selects a training set
    while True:
        try:
            if (bmi < 18.5):
                print(
                    "\nЗа результатами ІМТ вам доступний сет тренувань для «набору ваги»")
                set = 3
            elif (bmi_value >= 18.5 and bmi_value < 25):
                set = float(
                    input("Виберіть що вас цікавить(зниження-1 підтримка-2 набір-3): "))
                # Checking the correctness of variables
                if not (set == 1 or set == 2 or set == 3):
                    raise ValueError  # ("Ви ввели не коректну команду...")
            elif (bmi_value >= 25 and bmi_value < 30):
                set = float(input(
                    "Виберіть що вас цікавить(зниження-1 підтримка-2): "))
                # Checking the correctness of variables
                if not (set == 1 or set == 2):
                    raise ValueError  # ("Ви ввели не коректну команду...")
            return set
        except ValueError:
            print("Ви ввели не коректну команду...\nСпробуйте ще раз.\n")


def switch_case_set(set):  # checking and converting the selection set
    if set == 1:
        return "зниження ваги"
    elif set == 2:
        return "підтримки ваги"
    elif set == 3:
        return "набору ваги"
    else:
        raise ValueError("Помилка з обраним сетом тренувань...")


def choice_frequency():  # choosing the frequency of training per week
    while True:
        try:
            freq = float(
                input("Оберыть кількість тренувань на тиждень\n(доступно 1,2,або 3 рази):"))
            # Checking the correctness of variables
            if (freq == 1 or freq == 2 or freq == 3):
                return freq
            else:
                raise ValueError
        except ValueError:
            print("Ви ввели не коректну команду...\nСпробуйте ще раз.\n")


weight = weight_in()
height = height_in()


bmi_value = round(bmi_calculation(weight, height))          # Derivation of BMI

print(f"ІМТ = {bmi_value}")

# Analysis of BMI# Random recommendations for underweight
if (bmi_value < 18.5):
    recommendations_underweight = [
        "Ваш ІМТ є нижчим норми. Перед початком тренувань рекомендуємо звернутися до спеціаліста. Ви можете обрати план тренувань «набір ваги» і вводити у раціон більшу кількість калорій.",
        "Ваш ІМТ є заниженим. Перед початком тренувань рекомендуємо звернутися до спеціаліста для індивідуальної консультації.",
        "Ваш ІМТ є нижчим від норми. Рекомендуємо звернутися до спеціаліста для індивідуальної консультації."
    ]
    print(random.choice(recommendations_underweight))

elif (bmi_value >= 18.5 and bmi_value < 25):            # Random recommendations for normal weight
    recommendations_normal = [
        "Вітаємо, у вас ІМТ в межах норми. Ми рекомендуємо обрати наш план тренувань «підтримка ваги».",
        "Ваш ІМТ в нормі. Рекомендуємо план «підтримка ваги» для підтримки вашого стану.",
        "Вітаємо, у вас нормальний ІМТ. Ми рекомендуємо план тренувань «підтримка ваги»."
    ]
    print(random.choice(recommendations_normal))

elif (bmi_value >= 25 and bmi_value < 30):              # Recommendations for overweight
    recommendations_overweight = [
        "Ваш ІМТ є завищеним, рекомендуємо план тренувань «зниження ваги».",
        "Ваш ІМТ трохи перевищує норму. Рекомендуємо вам план тренувань «зниження ваги».",
        "Ваш ІМТ є трохи завищеним. Рекомендуємо вам план тренувань «зниження ваги»."
    ]
    print(random.choice(recommendations_overweight))

else:
    recommendations_obesity = [
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо звернутись до спеціаліста.",
        "У вас ІМТ, що вказує на ожиріння. Рекомендуємо звернутись до експерта.",
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо консультацію з дієтологом."
    ]
    print(random.choice(recommendations_obesity))


if (bmi_value < 18.5):            # we offer the user to choose a training set for: dropping, maintaining or gaining weight
    set = choice_set(bmi_value)

elif (bmi_value >= 18.5 and bmi_value < 25):
    print("За результатами ІМТ ми пропонуємо сет тренувань для «зниження ваги» «підтримки ваги» «набору ваги»")
    set = choice_set(bmi_value)

elif (bmi_value >= 25 and bmi_value < 30):
    print("За результатами ІМТ ми пропонуємо сет тренувань для «зниження ваги» або «підтримки ваги» ")
    set = choice_set(bmi_value)
else:
    # we don’t take responsibility for obese people
    print("За результатами ІМТ нажаль ми неможемо запропонувати вам сет тренувань...")
    input("\n\nЩоб завершити натисніть Enter.\n")
    raise SystemExit  # exit the program

print(f"\nОбрано сет тренувань для {switch_case_set(set)}\n")

# user chooses the number of training sessions per week
frequency = choice_frequency()

print(f"Користувач обрав {frequency} тренування на тиждень")
