from abc import ABC, abstractmethod
from models.bmi import BMIModel


class StorageInterface(ABC):
    @abstractmethod
    def save_user(self, user_id: str, phone_number: str) -> bool:
        pass

    @abstractmethod
    def save_bmi_record(self, user_id: int, BMI: BMIModel) -> bool:
        pass

    @abstractmethod
    def bmi_exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
