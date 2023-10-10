import json
import os

from config import RESULTS_PATH, RESULTS_DATA_FILE_TYPE, DATABASE_NAME


def generate_new_name():
    i = 0
    while True:
        res_path = os.sep.join([RESULTS_PATH, f"{DATABASE_NAME}_{i}{RESULTS_DATA_FILE_TYPE}"])
        if os.path.isfile(res_path):
            i += 1
            continue
        break
    return res_path


def find_latest_result():
    i = 0
    while True:
        res_path = os.sep.join([RESULTS_PATH, f"{DATABASE_NAME}_{i}{RESULTS_DATA_FILE_TYPE}"])
        if os.path.isfile(res_path):
            i += 1
            continue
        break
    return os.sep.join([RESULTS_PATH, f"{DATABASE_NAME}_{i - 1}{RESULTS_DATA_FILE_TYPE}"])
