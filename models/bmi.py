class BMIModel:
    def __init__(
        self,
        weight: float,
        height: float,
    ):
        self.weight = weight
        self.height = height / 100

    def validate(self):
        if not (0 < self.height <= 3 and 0 < self.weight <= 300):
            raise ValueError("Будь ласка, введіть реалістичні значення зросту та ваги.")
        return round(self.weight / (self.height**2), 2)

    def calculate_bmi(self) -> float:
        bmi = self.weight / ((self.height / 100) ** 2)
        return round(bmi, 1)

    def bmi_category(self) -> str:
        bmi_value = self.calculate_bmi()

        if bmi_value < 18.5:
            return "Недостатня вага"
        elif 18.5 <= bmi_value > 24.9:
            return "Нормальна вага"
        elif 25 <= bmi_value > 29.9:
            return "Надмірна вага"
        else:
            return "Ожиріння"
