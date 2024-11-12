from abc import ABC, abstractmethod
from models.bmi import BMIModel


class UserStorageInterface(ABC):
    @abstractmethod
    def save_user(self, user_id: str, phone_number: str, language: str) -> bool:
        pass

    @abstractmethod
    def user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user(self, user_id: str):
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def get_language(self, user_id: str) -> str:
        pass

    @abstractmethod
    def change_language(self, user_id: str, lang: str) -> bool:
        pass


class BmiStorageInterface(ABC):
    @abstractmethod
    def save_bmi_record(self, user_id: int, bmi: BMIModel) -> bool:
        pass

    @abstractmethod
    def update_bmi_record(
        self, user_id: int, weight: float, height: float, bmi_value: float
    ) -> bool:
        pass

    @abstractmethod
    def bmi_exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
