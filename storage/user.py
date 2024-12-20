import psycopg2
from psycopg2 import sql
from config.config import config
from storage.storage import UserStorageInterface
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="user_storage.log")


class UserStorage(UserStorageInterface):
    TABLE_USERS = "users"
    TABLE_BMI_RECORDS = "bmi_records"

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )

    def save_user(self, user_id: str, phone_number: str, language: str) -> bool:
        query = sql.SQL(
            """
            INSERT INTO {table} (user_id, phone_number, language)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET phone_number = EXCLUDED.phone_number,
                language = EXCLUDED.language
            """
        ).format(table=sql.Identifier(self.TABLE_USERS))

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (user_id, phone_number, language))
            logger.info("Successfully saved/updated user %s", user_id)
            return True
        except Exception as e:
            logger.error("Error saving user %s: %s", user_id, e)
            return False

    def user_exists(self, user_id: str) -> bool:
        query = sql.SQL(
            """
            SELECT COUNT(*) FROM {table} WHERE user_id = %s
            """
        ).format(table=sql.Identifier(self.TABLE_USERS))

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    count = cursor.fetchone()[0]
            logger.info("User exists check for %s: %s", user_id, count > 0)
            return count > 0
        except Exception as e:
            logger.error("Error checking if user exists %s: %s", user_id, e)
            return False

    def get_user_bmi_value(self, user_id: str):
        query = sql.SQL(
            """
            SELECT bmi_value FROM {table} WHERE user_id = %s
            """
        ).format(table=sql.Identifier(self.TABLE_BMI_RECORDS))

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    bmi_value = cursor.fetchone()
                    if bmi_value:
                        if bmi_value < 18.5:
                            return "underweight"
                        elif 18.5 <= bmi_value <= 24.9:
                            return "normal"
                        elif 25 <= bmi_value <= 29.9:
                            return "overweight"
                        else:
                            return "obesity"
                    logger.warning("User %s not found.", user_id)
                    return None
        except Exception as e:
            logger.error("Error fetching user %s: %s", user_id, e)
            return None

    def get_user(self, user_id: str):
        query = sql.SQL(
            """
            SELECT user_id, phone_number, language FROM {table} WHERE user_id = %s
            """
        ).format(table=sql.Identifier(self.TABLE_USERS))
        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    user = cursor.fetchone()
                    if user:
                        logger.info("Fetched user %s successfully.", user_id)
                        return {
                            "user_id": user[0],
                            "phone_number": user[1],
                            "language": user[2],
                        }
                    logger.warning("User %s not found.", user_id)
                    return None
        except Exception as e:
            logger.error("Error fetching user %s: %s", user_id, e)
            return None

    def get_language(self, user_id: str) -> str:
        user = self.get_user(user_id)
        if user:
            return user["language"]
        logger.warning("Language not found for user %s.", user_id)
        return None

    def change_language(self, user_id: str, lang: str) -> bool:
        query = sql.SQL(
            """
            UPDATE {table}
            SET language = %s
            WHERE user_id = %s
            """
        ).format(table=sql.Identifier(self.TABLE_USERS))

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (lang, user_id))
                    if cursor.rowcount > 0:
                        logger.info(
                            "Successfully changed language for user %s to %s",
                            user_id,
                            lang,
                        )
                        return True
                    else:
                        logger.warning(
                            "User %s not found, language change failed.", user_id
                        )
                        return False
        except Exception as e:
            logger.error("Error changing language for user %s: %s", user_id, e)
            return False

    def close(self) -> None:
        if self.conn:
            logger.info("Closing database connection.")
            self.conn.close()
