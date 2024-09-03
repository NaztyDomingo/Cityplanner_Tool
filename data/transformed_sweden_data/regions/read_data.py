import pandas as pd


def read_file(file_path):
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    return data
