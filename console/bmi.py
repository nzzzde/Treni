import random

weight = float(input("Введіть вагу: "))					#User enters weight
height = float(input("Введіть ріст в см: "))/100		#User enters height

if not (0 <= height < 3 and 0 <= weight <= 300):		#Checking the correctness of variables
	raise ValueError("Будь ласка, введіть реалістичні значення зросту та ваги.")

bmi_value = weight / (height ** 2)						#Calculation of BMI
print(bmi_value)										#Derivation of BMI

#It is necessary to add recommendations according to the result of BMI
if bmi_value < 18.5:				#Analysis of BMI
        print("Недостатня вага")
	# Random recommendations for underweight
	recommendations_underweight = [
        "Ваш ІМТ є нижчим норми. Перед початком тренувань рекомендуємо звернутися до спеціаліста. Ви можете обрати план тренувань «набір ваги» і вводити у раціон більшу кількість калорій.",
        "Ваш ІМТ є заниженим. Перед початком тренувань рекомендуємо звернутися до спеціаліста для індивідуальної консультації.",
        "Ваш ІМТ є нижчим від норми. Рекомендуємо звернутися до спеціаліста для індивідуальної консультації."
    ]
    print(random.choice(recommendations_underweight))
elif bmi_value >= 18.5 and bmi_value < 24.9:
        print("Нормальна вага")
        # Random recommendations for normal weight
    recommendations_normal = [
        "Вітаємо, у вас ІМТ в межах норми. Ми рекомендуємо обрати наш план тренувань «підтримка ваги».",
        "Ваш ІМТ в нормі. Рекомендуємо план «підтримка ваги» для підтримки вашого стану.",
        "Вітаємо, у вас нормальний ІМТ. Ми рекомендуємо план тренувань «підтримка ваги»."
    ]
    print(random.choice(recommendations_normal))
elif bmi_value >=25 and bmi_value  < 29.9:
        print("Надмірна вага")
        recommendations_overweight = [
        "Ваш ІМТ є завищеним, рекомендуємо план тренувань «зниження ваги».",
        "Ваш ІМТ трохи перевищує норму. Рекомендуємо вам план тренувань «зниження ваги».",
        "Ваш ІМТ є трохи завищеним. Рекомендуємо вам план тренувань «зниження ваги»."
    ]
        print(random.choice(recommendations_overweight))
else: 
        print("Ожиріння")
	recommendations_obesity = [
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо звернутись до спеціаліста та обрати план «зниження ваги».",
        "У вас ІМТ, що вказує на ожиріння. Рекомендуємо обрати план тренувань «зниження ваги».",
        "Ваш ІМТ свідчить про ожиріння. Рекомендуємо консультацію з дієтологом і план «зниження ваги»."
    ]
         print(random.choice(recommendations_obesity))
