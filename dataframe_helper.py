import pandas as pd
import os
import filehandler_helper as fh

def order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) == 11:
        list_with_columns = ['Year',
                            'Region',
                            'Population',
                            'Waste And Sewage',
                            'Machinery',
                            'Electricity And District Heating',
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
                            'Waste And Sewage',
                            'Machinery',
                            'Electricity And District Heating',
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
    word = word.capitalize()
    return word

def reverse_special_chars_finish(word: str) -> str:
    word = word.upper()
    replacements =  {'AE': 'Ä', 'OE': 'Ö', 'AA': 'Å'}
    for char, replacement in replacements.items():
        word = word.replace(char, replacement)
    word = word.capitalize()
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

def make_list_with_alternating_steps(indices: list, increments: list, amount_of_times_to_repeat_slicing: int) -> list:
    result = indices.copy()
    last_value = indices[-1]
    
    for i in range(amount_of_times_to_repeat_slicing): 
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

def remove_rows_from_not_unique_series(series: pd.Series, amount_of_rows_to_keep: int) -> pd.Series:    
    total_rows_per_slice = 0
    last_i = None

    for i in series:
        if total_rows_per_slice >= amount_of_rows_to_keep and i != last_i:
            break
        last_i = i
        total_rows_per_slice += 1

    rows_step_count = total_rows_per_slice - amount_of_rows_to_keep

    total_series_amount = sum(1 for index, _ in enumerate(series, 1) if index % amount_of_rows_to_keep == 0)

    indices = [amount_of_rows_to_keep, total_rows_per_slice]
    indices = make_list_with_alternating_steps(indices, [amount_of_rows_to_keep, rows_step_count], total_series_amount*2)

    data_list = series.tolist()
    
    # Include the end of the list
    indices = sorted(set(indices + [len(data_list)]))
    
    # Split the list based on indices
    split_lists = [data_list[i:j] for i, j in zip([0] + indices[:-1], indices)]
    
    filtered_list = [sublist for sublist in split_lists if len(sublist) == amount_of_rows_to_keep]
    
    flat_list = [item for sublist in filtered_list for item in sublist]

    series = pd.Series(flat_list)

    return series

def split_dataframe_and_transpose(df: pd.DataFrame, chunk_size: int) -> pd.DataFrame:
    dfs = [df.iloc[i:i + chunk_size].reset_index(drop=True) for i in range(0, len(df), chunk_size)]
    
    df_combined = dfs[0]
    df_combined.set_index(df.columns[0], inplace=True)
        
    for df in dfs[1:]:
        df.set_index(df.columns[0], inplace=True)
        
        df_combined = pd.concat([df_combined, df], axis=1)
            
    df_combined.reset_index(inplace=True)    
    df_combined = df_combined.transpose()
    return df_combined

def make_custom_csv_file_from_many_files(custom_csv_filename: str, filepath_input: str, filepath_output: str, split_word: str) -> None:
    list_with_files = fh.get_list_with_names_from_folder(filepath_input)

    output_df = pd.DataFrame()

    for file in list_with_files:
        filepath_of_file = os.path.join(filepath_input, file)
        df = pd.read_csv(filepath_of_file, header = 1)
        first_column = df.columns[0]
        region, column_name = first_column.split(split_word)
        column_name = split_word + column_name
        df.rename(columns={first_column: column_name}, inplace=True)
        df['Region'] = region
        output_df = pd.concat([output_df, df])
        
    file_output = os.path.join(filepath_output, custom_csv_filename)
    output_df.to_csv(file_output, index=False)