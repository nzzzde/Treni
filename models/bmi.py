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
        if not (100 < self.height <= 300 and 30 < self.weight <= 300):
            return False
        return True

    def calculate_bmi(self) -> float:
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters**2)
        self.calculated_bmi = bmi
        return self.calculated_bmi

    def bmi_category(self) -> str:
        bmi_value = self.calculate_bmi()

        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value <= 25:
            return "Normal weight"
        elif 25 < bmi_value < 30:
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
        elif 18.5 <= bmi_value <= 25:
            return translations["recommendations_normal"][self.lang]
        elif 25 < bmi_value < 30:
            return translations["recommendations_overweight"][self.lang]
        else:
            return translations["recommendations_obesity"][self.lang]

    def get_category(self) -> str:
        """Returns the BMI category based on the calculated BMI."""
        bmi_value = self.calculated_bmi or self.calculate_bmi()

        if bmi_value < 18.5:
            return "underweight"
        elif 18.5 <= bmi_value <= 25:
            return "normal"
        elif 25 < bmi_value < 30:
            return "overweight"
        else:
            return "obesity"

    def get_recommendation(self) -> str:
        bmi_value = self.calculate_bmi()
        recommendations = self._recommendations_by_bmi(bmi_value)
        return random.choice(recommendations)

    def _recommendations_by_bmi(self, bmi_value: float):
        if bmi_value < 18.5:
            return translations["recommendations_underweight"][self.lang]
        elif 18.5 <= bmi_value <= 25:
            return translations["recommendations_normal"][self.lang]
        elif 25 < bmi_value < 30:
            return translations["recommendations_overweight"][self.lang]
        else:
            return translations["recommendations_obesity"][self.lang]

    def get_videos_for_bmi_category(bmi_category: str) -> list:
        videos = []
        if bmi_category == "normal":
            videos = [
                "n_keep_set1_p1.MP4",
                "n_keep_set1_p2.MP4",
                "n_keep_set2_p1.MP4",
                "n_keep_set2_p2.MP4",
                "n_keep_set3_p1.MP4",
                "n_keep_set3_p2.MP4",
                "n_lg_set1_p1.MP4",
                "n_lg_set1_p2.MP4",
                "n_Ig_set1_p1.MP4",
                "n_Ig_set1_p2.MP4",
                "n_Ig_set2_p1.MP4",
                "n_Ig_set2_p2.MP4",
                "n_Ig_set3_p1.MP4",
                "n_Ig_set3_p2.MP4",
            ]
        elif bmi_category == "underweight":
            videos = ["uw_set1.MP4", "uw_set2.MP4", "uw_set3.MP4"]
        elif bmi_category == "overweight":
            videos = [
                "ow_set1_p1.MP4",
                "ow_set1_p2.MP4",
                "ow_set2_p1.MP4",
                "ow_set2_p2.MP4",
                "ow_set3_p1.MP4",
                "ow_set3_p2.MP4",
            ]
        return videos
