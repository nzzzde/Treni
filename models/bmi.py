import random
from translations.translations import translations


class BMIModel:
    def __init__(self, user_id: int, weight: float, height: float, lang: str):
        self.user_id = user_id
        self.weight = weight
        self.height = height
        self.lang = lang
        self.calculated_bmi = None

    def validate(self) -> bool:
        if not (0 < self.height <= 300 and 0 < self.weight <= 300):
            return False
        return True

    def calculate_bmi(self) -> float:
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters**2)
        self.calculated_bmi = round(bmi, 1)
        return self.calculated_bmi

    def bmi_category(self) -> str:
        bmi_value = self.calculate_bmi()

        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value <= 24.9:
            return "Normal weight"
        elif 25 <= bmi_value <= 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def get_recommendation(self) -> str:
        bmi_value = self.calculate_bmi()
        recommendations = self._recommendations_by_bmi(bmi_value)
        return random.choice(recommendations)

    def _recommendations_by_bmi(self, bmi_value: float):
        if bmi_value < 18.5:
            return translations["recommendations_underweight"][self.lang]
        elif 18.5 <= bmi_value <= 24.9:
            return translations["recommendations_normal"][self.lang]
        elif 25 <= bmi_value <= 29.9:
            return translations["recommendations_overweight"][self.lang]
        else:
            return translations["recommendations_obesity"][self.lang]
