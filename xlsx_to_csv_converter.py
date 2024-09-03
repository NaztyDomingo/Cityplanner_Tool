import pandas as pd
import filehandler_helper as fh
import numpy as np
import os

def convert_single_file(input_folder: str, output_folder: str, filename_without_extension: str) -> None:
    input_filename = filename_without_extension + '.xlsx'
    output_filename = filename_without_extension + '.csv'
    filepath = fh.get_path_of_file(input_folder, input_filename)

    df = pd.read_excel(filepath, index_col=2)
    output_filepath = fh.get_path_of_file(output_folder, output_filename)
    df.to_csv(output_filepath)

def convert_list_with_files(list_with_files: np.array, input_folder_path: str, output_folder_path: str) -> None:
    for file in list_with_files:
        filepath = os.path.join(input_folder_path, file)
        df = pd.read_excel(filepath)
        filename, extension = os.path.splitext(file)
        extension = '.csv'
        filename = filename + extension
        filepath = os.path.join(output_folder_path, filename)
        df.to_csv(filepath, header=False)