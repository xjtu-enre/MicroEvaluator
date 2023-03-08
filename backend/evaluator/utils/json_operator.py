import json
import os.path
from pathlib import Path


def read_folder(folder_path, measure_name, dep_name):
    try:
        folder = Path(folder_path)
        if folder.exists():
            with open(os.path.join(folder_path, measure_name), 'r', encoding='utf-8') as f:
                measure_json_dict = json.load(f, strict=False)
            with open(os.path.join(folder_path, dep_name), 'r', encoding='utf-8') as f:
                dep_json_dict = json.load(f, strict=False)
        else:
            measure_json_dict = dict()
            dep_json_dict = dict()
    except (FileExistsError, FileNotFoundError, PermissionError):
        measure_json_dict = dict()
        dep_json_dict = dict()
    return measure_json_dict, dep_json_dict


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_dict = json.load(f, strict=False)
    except (FileExistsError, FileNotFoundError, PermissionError):
        json_dict = dict()
    return json_dict


def write_result_to_json(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4)