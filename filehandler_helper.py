import os
import numpy as np
import re

# All pathin is taking place within the 'data' folder!

def get_path_of_file(folder: str, filename: str) -> str:
    FILEPATH = os.path.dirname(os.path.realpath(__file__))
    FOLDER = folder
    FILENAME = filename
    return os.path.join(FILEPATH, 'data', FOLDER, FILENAME)

def get_path_of_folder(folder: str) -> str:
    FILEPATH = os.path.dirname(os.path.realpath(__file__))
    FOLDER = folder
    return os.path.join(FILEPATH, 'data', FOLDER)

def get_list_with_names_from_folder(filepath: str) -> np.array:
    return os.listdir(filepath)

def get_current_filepath() -> str:
    return os.path.dirname(os.path.realpath(__file__))

def return_filepath_joined_with_file(current_filepath: str, filename: str) -> str:
    return os.path.join(current_filepath, filename)

def search_folder_get_list_with_foldernames(search_string: str, filepath_to_folder_to_search: str) -> list:
    regex = re.compile(f'{search_string}.*')
    folders = get_list_with_names_from_folder(filepath_to_folder_to_search)
    matching_folders = [folder for folder in folders if regex.search(folder)]
    return matching_folders