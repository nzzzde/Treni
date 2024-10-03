import logging
from psycopg2 import sql
from storage.storage import StorageInterface
from db.db_pool import DatabasePool
from models.bmi import BMIModel

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BmiStorage(StorageInterface):
    TABLE_BMI_RECORDS = "bmi_records"

    def __init__(self):
        self.db_pool = DatabasePool()

    def save_bmi_record(
        self,
        user_id: int,
        BMI: BMIModel,
    ) -> bool:
        conn = self.db_pool.get_connection()
        query = sql.SQL(
            """
			INSERT INTO {table} (user_id, weight, height, bmi_value)
			VALUES (%s, %s, %s, %s)
		"""
        ).format(table=sql.Identifier(self.TABLE_BMI_RECORDS))

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query, (user_id, BMI.weight, BMI.height, BMI.calculated_bmi)
                    )
            return True
        except Exception as e:
            logger.error("Error saving BMI record for user %s: %s", user_id, e)
            return False
        finally:
            self.db_pool.put_connection(conn)

    def save_user(self, user_id: str, phone_number: str) -> bool:
        return True

    def bmi_exists(self, user_id: int) -> bool:
        conn = self.db_pool.get_connection()
        query = sql.SQL(
            """
			SELECT COUNT(*) FROM {table} WHERE user_id = %s
		"""
        ).format(table=sql.Identifier(self.TABLE_BMI_RECORDS))

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            logger.error(
                "Error checking if BMI record exists for user %s: %s", user_id, e
            )
            return False
        finally:
            self.db_pool.put_connection(conn)

    def close(self) -> None:
        self.db_pool.close_all()
