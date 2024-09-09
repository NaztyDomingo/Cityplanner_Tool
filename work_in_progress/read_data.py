import pandas as pd


def read_file(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    return data

