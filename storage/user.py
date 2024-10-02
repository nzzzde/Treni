from abc import ABC
import psycopg2
from psycopg2 import sql
from config.config import config
from storage.storage import StorageInterface
import logging

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class UserStorage(StorageInterface):
    TABLE_USERS = "users"

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )

    def save_user(self, user_id: str, phone_number: str) -> bool:
        query = sql.SQL(
            """
			INSERT INTO {table} (user_id, phone_number)
			VALUES (%s, %s)
			ON CONFLICT (user_id) DO NOTHING
		"""
        ).format(table=sql.Identifier(self.TABLE_USERS))

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (user_id, phone_number))
            return True
        except Exception as e:
            logger.error("Error saving user %s: %s", user_id, e)
            return False

    def save_bmi_record(
        self, user_id: str, weight: float, height: float, bmi_value: float
    ) -> bool:
        logger.error("BMI record saving not implemented")
        return False

    def bmi_exists(self, user_id: int) -> bool:
        pass

    def close(self) -> None:
        if self.conn:
            self.conn.close()
