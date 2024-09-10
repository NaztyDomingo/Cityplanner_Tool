import pandas as pd
import transform as t
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'sweden_cities_emission.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'sweden_cities_emissions.csv')

def preprocess_column(column: pd.Series) -> pd.Series:
    column = column.astype(str)
    return column.str.replace(' ', '', regex=False)

def convert_emissions(data: pd.DataFrame) -> pd.DataFrame:
    columns_to_convert = [
        'Waste And Sewage', 'Machinery', 'Electricity And District Heating',
        'Agriculture', 'Transportation', 'Industry'
    ]
    
    for column in columns_to_convert:
        data[column] = preprocess_column(data[column])
        data[column] = pd.to_numeric(data[column], errors='coerce')
    
    df_2022 = data[data['Year'] == 2022]
    
    for index, row in df_2022.iterrows():
        population = row['Population']
        for column in columns_to_convert:
            data.at[index, column] = (row[column] * population) / 1_000_000
            
    data.loc[data['Year'] == 2022] = data.loc[data['Year'] == 2022].round(1)
    
    return data

data = pd.read_csv(file_path)

print(data)

data = t.rename_reorder_columns(data)
print(data)

t.data_to_csv(data)
