from psycopg2 import sql
from db.db_pool import DatabasePool
from models.bmi import BMIModel
from storage.storage import BmiStorageInterface
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="bmi_storage.log")


class BmiStorage(BmiStorageInterface):
    TABLE_BMI_RECORDS = "bmi_records"

    def __init__(self):
        self.db_pool = DatabasePool()

    def save_bmi_record(self, user_id: int, bmi: BMIModel) -> bool:
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
                        query, (user_id, bmi.weight, bmi.height, bmi.calculated_bmi)
                    )
            logger.info("Successfully saved BMI record for user %s", user_id)
            return True
        except Exception as e:
            logger.error("Error saving BMI record for user %s: %s", user_id, e)
            return False
        finally:
            self.db_pool.put_connection(conn)

    def update_bmi_record(
        self, user_id: int, weight: float, height: float, bmi_value: float
    ) -> bool:
        conn = self.db_pool.get_connection()
        query = sql.SQL(
            """
            UPDATE {table}
            SET weight = %s, height = %s, bmi_value = %s
            WHERE user_id = %s
            """
        ).format(table=sql.Identifier(self.TABLE_BMI_RECORDS))

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (weight, height, bmi_value, user_id))
            logger.info("Successfully updated BMI record for user %s", user_id)
            return True
        except Exception as e:
            logger.error("Error updating BMI record for user %s: %s", user_id, e)
            return False
        finally:
            self.db_pool.put_connection(conn)

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
            logger.info("BMI record exists check for user %s: %s", user_id, count > 0)
            return count > 0
        except Exception as e:
            logger.error(
                "Error checking if BMI record exists for user %s: %s", user_id, e
            )
            return False
        finally:
            self.db_pool.put_connection(conn)

    def close(self) -> None:
        logger.info("Closing all database connections.")
        self.db_pool.close_all()
