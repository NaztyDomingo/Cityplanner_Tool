import pandas as pd

def order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) == 11:
        list_with_columns = ['Year',
                            'Region',
                            'Population',
                            'Waste and Sewage',
                            'Machinery',
                            'Electricity and District Heating',
                            'Other Heating',
                            'Agriculture',
                            'Transportation',
                            'Industry',
                            'Total Emissions']
        return df[list_with_columns]
    else:
        list_with_columns = ['Year',
                             'City',
                            'Region',
                            'Population',
                            'Waste and Sewage',
                            'Machinery',
                            'Electricity and District Heating',
                            'Other Heating',
                            'Agriculture',
                            'Transportation',
                            'Industry',
                            'Total Emissions']
        return df[list_with_columns]

def replace_special_chars(word: str) -> str:
    word = word.upper()
    replacements = {'Ä': 'AE', 'Ö': 'OE', 'Å': 'AA'}
    for char, replacement in replacements.items():
        word = word.replace(char, replacement)
    return word

def replace_word_to_camel_case(word: str) -> str:
    word = word.lower()
    word_capitalized = word.title()
    replacements = {word : word_capitalized}
    for char, replacement in replacements.items():
        word = word.replace(char, replacement)
    return word

def drop_columns(df: pd.DataFrame, columns_to_be_dropped: list) -> pd.DataFrame:
    df.drop(columns=columns_to_be_dropped, inplace=True, axis=1)
    return df