import random
import time
from datetime import datetime, timedelta

def weight_in():                            # User enters weight
    while True:
        wght = input("Введіть вагу: ")
        try:
            weight = float(wght)
        except ValueError:
            print("Вагу потрібно вводити числом! \nСпробуйте ще раз.\n")
        else:
            try:
                if (15 <= weight <= 300):        # Checking thecorrectness of variables
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
                if (0.3 <= height <= 3):        # Checking the correctnessof variables
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
 
def switch_case_set(set):  # checking and converting the selectionset
    if set == 1:
        return "зниження ваги"
    elif set == 2:
        return "підтримки ваги"
    elif set == 3:
        return "набору ваги"
    else:
        raise ValueError("Помилка з обраним сетом тренувань...")
 
def choice_frequency():  # choosing the frequency of training perweek
    while True:
        try:
            freq = float(
                input("Оберіть кількість тренувань на тиждень\n(доступно 1,2,або 3 рази):"))
            # Checking the correctness of variables
            if (freq == 1 or freq == 2 or freq == 3):
                return freq
            else:
                raise ValueError
        except ValueError:
            print("Ви ввели не коректну команду...\nСпробуйте ще раз.\n")

def select_training_sets(frequency):  #  selection of training depending on the frequency
    if frequency == 1:
        return [random.choice(training_sets)]  # One random set
    elif frequency == 2:
        return random.sample(training_sets, 2)  # Two unique sets without repetitions
    elif frequency == 3:
        return training_sets  # All three sets

def training_sets(bmi_value, frequency):
    if bmi_value < 18.5:
        print("Сети тренувань для набору ваги:\n")
        sets = [
            "Cет №1\nВипади в сторону 10 разів\nПідняття ніг 10 разів на кожну ногу\nПрисідання біля стіни 10 разів\nБіг на місці 2 хвилини\nЯгодичний міст 10 разів\nСупермен 30 секунд\nВелосипед 30 секунд\n",
            "Cет №2\nСтрибки з розведенням рук і ніг — 10 разів\nБіг на місці — 2 хвилини\nПрисідання біля стіни 10 разів\nПідняття ніг — 10 разів на кожну ногу\nСупермен 30 секунд\nВелосипед 30 секунд\n",
            "Cет №3\nБіг на місці — 2 хвилини\nБерпі — 7 разів\nПрисідання біля стіни 10 разів\nАльпініст — 20 секунд\nЯгодичний міст — 15 разів\nВипади в сторону — 10 разів\nПланка — 20 секунд\n"
        ]
    
    elif 18.5 <= bmi_value < 25:
        if set == 1:
            print("Сети тренувань для зниження ваги:\n")
        elif set == 2:
            print("Сети тренувань для підтримки ваги:\n")
        elif set == 3:
            print("Сети тренувань для набору ваги:\n")
        sets = [
            "Cет №1\nБіг на місці — 5 хвилин\nПрисідання — 20 раз\nЯгодичний міст — 20 раз\nПідняття ніг — 20 раз на кожну ногу\nСупермен — 1 хвилина\nСкручування — 20 раз\nВелосипед — 1 хвилина\nВіджимання — 10 раз\nПланка з ліктів — 30 секунд\nВипади — 20 раз\nВипади в сторону — 20 раз\n",
            "Cет №2\nБіг на місці — 5 хвилин\nСтрибки з розведенням рук і ніг — 10 раз\nЯгодичний міст — 20 раз\nПідняття ніг — 20 раз на кожну ногу\nСупермен — 1 хвилина\nПланка — 30 секунд\nВипади — 20 раз\nВипади в сторону — 20 раз\n",
            "Cет №3\nБіг на місці — 5 хвилин\nБерпі — 10 раз\nПрисідання — 30 раз\nАльпініст — 1 хвилина\nВіджимання — 10 раз\nСкручування — 20 раз\nВіджимання з планки — 30 секунд\nПідняття ніг з ліктевої планки — 30 секунд\nСупермен — 1 хвилина\n"
        ]
    
    else:
        if set == 1:
            print("Сети тренувань для зниження ваги:\n")
        elif set == 2:
            print("Сети тренувань для підтримки ваги:\n")
        sets = [
            "Cет №1\nБіг на місці — 5 хвилин\nСтрибки з розведенням рук і ніг — 20 раз\nСкручування — 35 раз\nБерпі — 15 раз\nВипади — 30 раз\nВипади в сторону — 30 раз\nАльпініст — 30 секунд\nЯгодичний міст — 35 раз\nПідняття ніг з ліктевої планки — 1 хвилина\nПланка з ліктів — 1 хвилина\nВелосипед — 2 хвилин\nВіджимання з планки — 1 хвилина\n",
            "Cет №2\nБіг на місці — 5 хвилин\nБерпі — 15 раз\nВипади — 30 раз\nВипади в сторону — 30 раз\nСупермен — 2 хвилини\nЯгодичний міст — 35 раз\nАльпініст — 30 секунд\nВелосипед — 2 хвилини\nВіджимання — 15 раз\nСкручування — 35 раз\n",
            "Cет №3\nБіг на місці — 5 хвилин\nСтрибки з розведенням рук і ніг — 15 раз\nПрисідання біля стіни — 15 раз\nВипади в сторону — 20 раз\nСкручування — 35 раз\nПланка — 45 секунд\nПідняття ніг — 30 раз на кожну ногу\nЯгодичний міст — 30 раз\n"
        ]
        # Select training sets based on frequency
    if frequency == 1:
        selected_sets = [random.choice(sets)]  # One random set
    elif frequency == 2:
        selected_sets = random.sample(sets, 2)  # Two unique sets
    else:
        selected_sets = sets  # All three sets

    for set_number, training_set in enumerate(selected_sets, 1):
        print(f"День {set_number}:\n{training_set}")

def select_days(frequency):  # Choosing days for training based onfrequency
    days_of_week = ["понеділок", "вівторок", "середа", "четвер", "п'ятниця", "субота", "неділя"]
    selected_days = []
    
    print(f"\nОберіть {int(frequency)} день(дні) для тренувань із наступних варіантів:")
    
    for idx, day in enumerate(days_of_week, start=1):
        print(f"{idx}. {day}")
 
    while len(selected_days) < frequency:
        try:
            choice = int(input(f"\nОберіть цифру дня який потрібен №{len(selected_days) + 1}: "))
            if 1 <= choice <= 7:
                selected_day = days_of_week[choice - 1]
                if selected_day not in selected_days:
                    selected_days.append(selected_day)
                else:
                    print("Цей день уже обрано. Оберіть інший.")
            else:
                raise ValueError
        except ValueError:
            print("Введено неправильний номер дня. Спробуйте ще раз.")
 
    print(f"\nВи обрали наступні дні для тренувань: {', '.join(selected_days)}")
    return selected_days

def Check_set_reminder_time():
    while True:
        try:
            reminder = input("Бажаєте встановити нагадування на певний час? (так/ні): ").lower()
                # Checking the correctness of variable
            if (reminder == 'так' or reminder == 'ні'):
                return reminder
            else:
                raise ValueError
        except ValueError:
                print("Ви ввели не коректну команду...\nСпробуйте ще раз.\n")    

def set_reminder(selected_days):  
    reminders = []
    for day in selected_days:
        while True:
            try:
                reminder_time = input(f"Введіть час для нагадування на {day} у форматі ЧЧ:ММ (24-годинний формат): ")
                reminder_hour, reminder_minute = map(int, reminder_time.split(":"))
                
                if 0 <= reminder_hour < 24 and 0 <= reminder_minute < 60:
                    
                    current_time = datetime.now()
                    current_day_index = current_time.weekday()
                    
                    target_day_index = ["понеділок", "вівторок", "середа", "четвер", "п'ятниця", "субота", "неділя"].index(day)

                    
                    days_ahead = (target_day_index - current_day_index + 7) % 7
                    reminder_day = current_time + timedelta(days=days_ahead)
                    
                    
                    reminder = reminder_day.replace(hour=reminder_hour, minute=reminder_minute, second=0, microsecond=0)
                    reminders.append((day, reminder))

                    
                    time_until_reminder = reminder - current_time
                    hours, remainder = divmod(time_until_reminder.seconds, 3600)
                    minutes = remainder // 60

                    
                    print(f"Нагадування встановлено на {day} о {reminder.strftime('%H:%M')} ({reminder.strftime('%Y-%m-%d')}).")
                    print(f"Залишилося: {time_until_reminder.days} днів, {hours} годин, {minutes} хвилин.\n")
                    break
                else:
                    print("Введено неправильний час. Спробуйте ще раз.")
            except ValueError:
                print("Введено неправильний формат. Спробуйте ще раз.")
    return reminders

def remind_training(reminders):
    print("Час для тренувань збережено!")
    while reminders:
        current_time = datetime.now()
        for day, reminder in reminders[:]:  
            if current_time >= reminder:
                print(f"\nНастав час для тренування! Починайте свій сет вправ на {day} о {reminder.strftime('%H:%M')}!")
                reminders.remove((day, reminder))  
        time.sleep(60) 

def check_for_help(): 
    help_text = """
    Довідник:
    1. Рекомендовані інтервали між вправами 20~30 секунд.
    2. Підтримуйте баланс води в організмі протягом дня.
    3. Дотримуйтесь частоти тренувань 1, 2 або 3 рази на тиждень.
    4. Утримуйтесь від суворих дієт.
    Пам'ятайте, що головне — почати: зробити перший маленький крок назустріч здоровому тілу і щасливому життю!
    """
    # User request
    key = input("Натисніть '0', якщо хочете переглянути довідник,натисніть '5',якщо бажаєте переглянути інформацію про бота або будь-яку іншу клавішу для виходу: ")
    
    if key == '0':  # If '0' is entered, we display the directory
        print(help_text)
        return True
    elif key == '5':
        inf_text = """
        Treni - ваш помічник на шляху до найкращої та найздоровішої версії себе. 
        Цей бот розрахує ваш індекс маси тіла та згідно нього та вашої мети підбере найкращі та найдієвіші тренування. 
        Також у нашому боті є можливість оновлювати дані, що відрізняє нас від інших схожих проектів. 
        А якщо ви захочете поділитися нашим ботом з своїми іноземними друзями, у нас є вбудована англійська, тож сміло діліться.
        Проектом Treni займалися найкращі студенти спеціальності “Кібербезпека” Львівської політехніки:
        • Хімчик Анастасія - проджект менеджер, слідкувала і направляла команду під час створення проекту.
        • Кучерук Ілля та Федас Данило - пайтон розробники, разом створювали прототип проекту в консолі.
        • Здебська Анастасія - пайтон розробник, перетворювала прототип у робочу версію проекту в телеграмі.
        • Федунів Яна - тестувальник, тестувала кожну нову версію на наявність помилок і збоїв, ламала там де це можливо і неможливо для того щоб вам цього не вдалось.
        • Шумада Софія - продукт менеджер та дизайнер, наповнювала проект текстами та ілюстраціями.
        
        Пам'ятайте, що головне — почати: зробити перший маленький крок назустріч здоровому тілу і щасливому життю!"""
        print(inf_text)
        return True
    else:
        return False
def edit_reminders(reminders):
    while True:
        print("\nВаші нагадування:")
        for index, (day, reminder) in enumerate(reminders):
            print(f"{index + 1}. {day} о {reminder.strftime('%H:%M')}")

        print("\nВиберіть дію:")
        print("1. Видалити нагадування")
        print("2. Редагувати нагадування")
        print("Щоб вийти введіть будь що")

        choice = input("Ваш вибір (1/2/...): ").lower()       
            
        if choice == '1':
            try:
                reminder_to_delete = int(input("Введіть номер нагадування, яке потрібно видалити: ")) - 1
                if 0 <= reminder_to_delete < len(reminders):
                    removed_day, removed_time = reminders.pop(reminder_to_delete)
                    print(f"Нагадування на {removed_day} о {removed_time.strftime('%H:%M')} видалено.")
                else:
                    print("Неправильний номер нагадування.")
            except ValueError:
                print("Введіть коректний номер.")
        elif choice == '2':
            try:
                reminder_to_edit = int(input("Введіть номер нагадування для редагування: ")) - 1
                if 0 <= reminder_to_edit < len(reminders):
                    new_time = input(f"Введіть новий час для нагадування на {reminders[reminder_to_edit][0]} у форматі ЧЧ:ММ (24-годинний формат): ")
                    new_hour, new_minute = map(int, new_time.split(":"))
                    
                    if 0 <= new_hour < 24 and 0 <= new_minute < 60:
                        current_time = datetime.now()
                        target_day = reminders[reminder_to_edit][0]
                        current_day_index = current_time.weekday()
                        target_day_index = ["понеділок", "вівторок", "середа", "четвер", "п'ятниця", "субота", "неділя"].index(target_day)

                        
                        days_ahead = (target_day_index - current_day_index + 7) % 7
                        reminder_day = current_time + timedelta(days=days_ahead)
                        new_reminder = reminder_day.replace(hour=new_hour, minute=new_minute, second=0, microsecond=0)
                        
                        reminders[reminder_to_edit] = (target_day, new_reminder)
                        print(f"Нагадування на {target_day} оновлено на {new_reminder.strftime('%H:%M')} ({new_reminder.strftime('%Y-%m-%d')}).")
                    else:
                        print("Введено неправильний час.")
                else:
                    print("Неправильний номер нагадування.")
            except ValueError:
                print("Введіть коректний номер.")
        else:
            check_for_help()
            break
 
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
 
elif (bmi_value >= 18.5 and bmi_value < 25):            # Randomrecommendations for normal weight
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
    print("За результатами ІМТ нажаль ми не можемо запропонувати вам сет тренувань...")
    input("\n\nЩоб завершити натисніть Enter.\n")
    raise SystemExit  # exit the program
 
print(f"\nОбрано сет тренувань для {switch_case_set(set)}\n")
 
# user chooses the number of training sessions per week
frequency = choice_frequency()

training_sets(bmi_value, frequency)
 
selected_days = select_days(frequency)   # Choice of training days

set_reminder_time = Check_set_reminder_time()
if set_reminder_time == "так":
    reminders = set_reminder(selected_days)
    edit_reminders(reminders)  
    remind_training(reminders)  
else:
    print("Нагадування не встановлено.")
    check_for_help()
    exit()