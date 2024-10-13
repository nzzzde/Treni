class UserModel:
    def __init__(self, user_id: int, phone_number: str = None, language: str = "en"):
        self.user_id = user_id
        self.phone_number = phone_number
        self.language = language
