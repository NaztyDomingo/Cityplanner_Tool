import pandas as pd
import os

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

def reverse_special_chars_finish(word: str) -> str:
    word = word.upper()
    replacements =  {'AE': 'Ä', 'OE': 'Ö', 'AA': 'Å'}
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

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={'Hinku calculation without emission credits': 'Year','Waste treatment': 'Waste And Sewage', 'total emissions. ktCO2e': 'Total Emissions', 'population': 'Population', 'total emissions, ktCO2e': 'Total Emissions'}, inplace=True)

    df['Transportation'] = df['Road transport'] + df['Water transport'] + df['Rail transport']
    df['Electricity And District Heating'] = df['Electricity'] + df['District heating']
    df['Other Heating'] = df['Electric heating'] + df['Oil heating'] + df['Other heating']

    df.drop(columns=['Road transport', 'Water transport', 'Rail transport','Electricity', 'District heating', 'Oil heating', 'Electric heating', 'Other heating'], inplace=True)
    
    df = df.round(1)
    df = order_dataframe(df)
    return df


def drop_columns(df: pd.DataFrame, columns_to_be_dropped: list) -> pd.DataFrame:
    df.drop(columns=columns_to_be_dropped, inplace=True, axis=1)
    return df

def change_values_in_multiple_files(folder_path: str, list_with_filenames: list, value_to_change: str, value_to_replace: str) -> None:
    for file in list_with_filenames:
        filepath_of_file = os.path.join(folder_path, file)
        df = pd.read_csv(filepath_of_file)
        for column in df.columns:
            df[column] = df[column].str.replace(value_to_change, value_to_replace)
        
        df.to_csv(filepath_of_file, index=False)

def make_list_with_alternating_steps(indices: list, increments: list, count: int) -> list:
    result = indices.copy()
    last_value = indices[-1]
    
    for i in range(count): 
        increment = increments[i % len(increments)]  # Alternate between increments
        last_value += increment
        result.append(last_value)
    
    return result

def remove_extra_rows_from_unique_series(series: pd.Series, amount_to_keep: int) -> pd.Series:
    series.reset_index(drop=True, inplace=True)

    limited_series = []
    
    for value in series.unique():
        limited_values = series[series == value].head(amount_to_keep)
        limited_series.append(limited_values)
        
    return pd.concat(limited_series, ignore_index=True)

def remove_extra_rows_from_not_unique_series(series: pd.Series, amount_of_rows_to_keep: int) -> pd.Series:    

    indices = [11, 17, 28, 34, 45, 51, 62, 68, 79, 85, 96, 102, 113, 119, 130, 136, 147, 153, 164, 170]
    indices = make_list_with_alternating_steps(indices, [amount_of_rows_to_keep, 6], 18)
    
    data_list = series.tolist()
    
    # Include the end of the list
    indices = sorted(set(indices + [len(data_list)]))
    
    # Split the list based on indices
    split_lists = [data_list[i:j] for i, j in zip([0] + indices[:-1], indices)]
    
    filtered_list = [sublist for sublist in split_lists if len(sublist) == 11]
    
    flat_list = [item for sublist in filtered_list for item in sublist]

    series = pd.Series(flat_list)

    return series