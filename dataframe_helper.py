import pandas as pd

def order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    list_with_columns = ['Year',
                        'Region',
                        'Population',
                        'Waste and Sewage',
                        'Machinery',
                        'Electricity and District Heating',
                        'Other heating',
                        'Agriculture',
                        'Transportation',
                        'Industry',
                        'Total Emissions']
    return df[list_with_columns]

def replace_special_chars(region_name: str) -> str:
    replacements = {'Ä': 'AE', 'Ö': 'OE', 'Å': 'AA'}
    for char, replacement in replacements.items():
        region_name = region_name.replace(char, replacement)
    return region_name