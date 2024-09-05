import read_data as rd
import pandas as pd

def converter(data: pd.DataFrame) -> pd.DataFrame:
    data['Population'] = data['Population'].str.replace(' ', '').astype(int)
    
    data['Total'] = data['Total'].str.replace(' ', '').astype(int)

    data['Total in kiloton'] = (data['Total'] * data['Population']) / 1_000_000

    return data


def transform_data(data: str) -> str:
    print(f"Columns available in transform_data: {data.columns.tolist()}")

    data['Total Emissions'] = data[['Heating','Electricity and District Heating', 'Industry', 'Transportation', 'Machinery', 'Product Use', 'Agriculture', 'Waste and Sewage']].sum(axis=1)

    
    return data
