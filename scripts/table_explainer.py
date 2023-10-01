import json
import logging
import os
from time import sleep

import pandas as pd
import openai
import glob

from common.prompts import (
    TABLE_CREATING_SYSTEM_PROMPT,
    TABLE_CREATING_USER_PROMPT
)

from config import (
    INPUT_PATH,
    OUTPUT_PATH,
    INPUT_DATA_FILE_TYPE,
    OUTPUT_DATA_FILE_TYPE,
    read_api_key
)

from common.utils import mkdir_if_not_exist


def columns_given(table: pd.DataFrame):
    return_string = ""
    for col_name in table.columns:
        return_string += f"{col_name}: {table[col_name].values}\n"
    return return_string


def generate_explanation(table):
    return openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
        {"role": "system", "content": TABLE_CREATING_SYSTEM_PROMPT},
        {"role": "user",
         "content": TABLE_CREATING_USER_PROMPT.format(columns=table.columns, sample=columns_given(table))}
    ], temperature=0)['choices'][0]['message']['content']


def table_explainer(table: pd.DataFrame(), table_name: str):
    """Gives an explanation for a table, generated using ChatGPT-3.5. The results are saved in the 'data' folder, named by the name of the table.
    :parameter table: A pandas dataframe consisting of 10 to 50 samples of a SQL table.
    Using rows with more information in them is recommended for the learning process.
    :parameter table_name: A string defining the schema and table name.
    Example: customer_schema.customer_satisfaction
    :returns None: The resulting explanation is saved in the data folder as a json file."""

    answer = generate_explanation(table)
    try:
        answer = json.loads(answer)
        answer['table_name'] = table_name
        mkdir_if_not_exist(OUTPUT_PATH)
        file_path = os.sep.join([OUTPUT_PATH, f"{table_name}{OUTPUT_DATA_FILE_TYPE}"])
        with open(file_path, "w") as outfile:
            outfile.write(json.dumps(answer))
    except Exception as e:
        logging.error(e)


def get_table_name(table_path):
    return table_path.split(os.sep)[-1].replace(INPUT_DATA_FILE_TYPE, "")


def main():
    openai.api_key = read_api_key()
    for table_path in glob.glob(f"{INPUT_PATH}/*"):
        table = pd.read_csv(table_path)
        table_explainer(table, get_table_name(table_path))
        sleep(20)


if __name__ == '__main__':
    main()
