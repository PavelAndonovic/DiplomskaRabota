import os
import sqlite3

import pandas as pd
from config import (
    DB_PATH,
    INPUT_PATH,
    INPUT_DATA_FILE_TYPE
)
from common.messages import (
    CONNECTED_TO_DB_MESSAGE,
    DB_CONNECTION_ERROR_MESSAGE,
    DB_CONNECTION_CLOSED_MESSAGE
)

from common.queries import (
    GET_SAMPLE_DATA_FROM_TABLE,
    GET_ALL_TABLE_NAMES
)

from common.utils import mkdir_if_not_exist

import logging

logging.basicConfig(level=logging.INFO)


def save_table_data(table_name, cursor, row_limit=50):
    cursor.execute(GET_SAMPLE_DATA_FROM_TABLE.format(table_name=table_name, row_limit=row_limit))
    column_names = [i[0] for i in cursor.description]
    record = cursor.fetchall()
    data = pd.DataFrame(columns=column_names, data=record)
    mkdir_if_not_exist(INPUT_PATH)
    data.to_csv(os.sep.join([INPUT_PATH, f"{table_name}{INPUT_DATA_FILE_TYPE}"]), index=False)


def main():
    try:
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        logging.info(CONNECTED_TO_DB_MESSAGE)
        cursor.execute(GET_ALL_TABLE_NAMES)
        table_names = cursor.fetchall()
        for table in table_names:
            save_table_data(table[0], cursor)
        cursor.close()

    except sqlite3.Error as error:
        logging.error(DB_CONNECTION_ERROR_MESSAGE, error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logging.info(DB_CONNECTION_CLOSED_MESSAGE)


if __name__ == "__main__":
    main()
