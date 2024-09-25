weight = float(input("Введіть вагу: "))					#User enters weight
height = float(input("Введіть ріст в см: "))/100		#User enters height

if not (0 <= height < 3 and 0 <= weight <= 300):		#Checking the correctness of variables
	raise ValueError("Будь ласка, введіть реалістичні значення зросту та ваги.")

bmi_value = weight / (height ** 2)						#Calculation of BMI
print(bmi_value)										#Derivation of BMI

#It is necessary to add recommendations according to the result of BMI
if bmi_value < 18.5:				#Analysis of BMI
        print("Недостатня вага")		
elif bmi_value >= 18.5 and bmi_value < 24.9:
        print("Нормальна вага")
elif bmi_value >=25 and bmi_value  < 29.9:
        print("Надмірна вага")
else: 
        print("Ожиріння")
