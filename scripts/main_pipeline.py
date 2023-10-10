import json
import logging
import os

from dotenv import load_dotenv
import openai

import data_collector
import table_explainer
import query_generator

from common.question import QUESTION
from common.result_naming import find_latest_result

from config import (
    DB_PATH,
    DATABASE_NAME,
    INPUT_PATH,
    OUTPUT_PATH
)

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not os.path.isfile(DB_PATH):
        raise Exception(f'Spider database with the name {DATABASE_NAME} doesn\'t exist. '
                        f'Please try another name in config.DATABASE_NAME')

    if not os.path.isdir(INPUT_PATH):
        logging.info('Running data collector')
        data_collector.main()

    if not os.path.isdir(OUTPUT_PATH):
        logging.info('Running table explainer')
        table_explainer.main()

    logging.info('Running query generator')
    query_generator.main(question=QUESTION)

    with open(find_latest_result()) as f:
        result = json.load(f)

    print(result['query'])
