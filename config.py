import os

from dotenv import load_dotenv

from common.enumeration import FileType


def read_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

DATABASE_NAME = 'tracking_grants_for_research'

DB_PATH = os.sep.join(["..", "data", "spider", "database", DATABASE_NAME, f"{DATABASE_NAME}.sqlite"])

INPUT_PATH = os.sep.join(["..", "data", "input_data", DATABASE_NAME])
OUTPUT_PATH = os.sep.join(["..", "data", "output_data", DATABASE_NAME])
INDEX_PATH = os.sep.join(["..", "index", DATABASE_NAME])
RESULTS_PATH = os.sep.join(["..", "results", DATABASE_NAME])

INPUT_DATA_FILE_TYPE = FileType.CSV.value
OUTPUT_DATA_FILE_TYPE = FileType.JSON.value
RESULTS_DATA_FILE_TYPE = FileType.JSON.value

SIMILARITY_TOP_K_VALUE = 10