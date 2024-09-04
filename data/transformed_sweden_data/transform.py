import read_data as rd
import pandas as pd
import glob
import os


CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emission_all_regions_2022.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'region_emissions_2022.csv')

def converter(data: pd.DataFrame) -> pd.DataFrame:
    data['Population'] = data['Population'].str.replace(' ', '').astype(int)
    data['Total'] = data['Total'].str.replace(' ', '').astype(int)
    data['Total in kiloton'] = (data['Total'] * data['Population']) / 1_000_000

    return data

def drop_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(columns=['Total', 'Product_use'])
    data = data.reset_index(drop=True)
    
    return data

def transform_columns(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = data.columns.str.replace('_', ' ').str.title()


def transform_data(data: str) -> str:
    data['Total Emissions'] = data[['Heating','Electricity and District Heating', 'Industry', 'Transportation', 'Machinery', 'Product Use', 'Agriculture', 'Waste and Sewage']].sum(axis=1)

    return data

def data_to_csv(data: pd.DataFrame) -> None:
    data.to_csv(output_file, index=False)



data = rd.read_file(file_path)

data = converter(data)
data = drop_columns(data)
data = transform_columns(data)

data_to_csv(data)
