import pandas as pd

def order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
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

def replace_special_chars(word: str) -> str:
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