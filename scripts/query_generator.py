import json
import os

from dotenv import load_dotenv

import table_evaluator_llama
import openai

from common.prompts import PROMPT_QUERY_GENERATOR
from common.question import QUESTION
import logging

from common.result_naming import generate_new_name
from config import (
    OUTPUT_PATH,
    OUTPUT_DATA_FILE_TYPE,
    RESULTS_PATH,
)

from common.utils import mkdir_if_not_exist


def get_indexes_from_folder(llama_evaluated_tables: str):
    logging.info("Started get_indexes_from_folder")
    indexes = []
    relevant_columns = []
    for row in llama_evaluated_tables.split('\n'):
        table_name = row.split(':')[0]
        if table_name == "":
            continue
        with open(os.sep.join([OUTPUT_PATH, f"{table_name}{OUTPUT_DATA_FILE_TYPE}"]), 'r') as f:
            indexes.append(f.readlines())
        relevant_columns.append(row.split(': ')[1])
    return indexes, relevant_columns


def create_query_explaining_prompt(llama_evaluated_tables, question):
    indexes, relevant_columns = get_indexes_from_folder(llama_evaluated_tables)
    print(indexes)

    return PROMPT_QUERY_GENERATOR.format(
        indexes=json.dumps(indexes),
        question=question
    )


def save_results(question, llama_evaluated_tables, answer):
    result = {
        'question': question,
        'llama_index_output': llama_evaluated_tables,
        'query': answer
    }
    mkdir_if_not_exist(RESULTS_PATH)
    with open(generate_new_name(), 'w') as f:
        f.write(json.dumps(result))


def main(question: str):
    llama_evaluated_tables = table_evaluator_llama.main(question)
    logging.info("Created llama_evaluated_tables")

    prompt = create_query_explaining_prompt(llama_evaluated_tables, question)

    answer = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )['choices'][0].message.content
    save_results(question, llama_evaluated_tables, answer)


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main(QUESTION)
