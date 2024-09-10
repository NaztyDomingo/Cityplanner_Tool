import filehandler_helper as fh
import xlsx_to_csv_converter as convert
import pandas as pd
import os
import dataframe_helper as dh

def main() -> None:
    _transform_regions_data()

    _tranform_cities_data()
    print('All files transformed...')

def _tranform_cities_data() -> None:
    # Converting finland cities file to csv
    convert.convert_single_file('finland_data', 'transformed_finland_data', 'finland_cities_emissions')

    filename = 'finland_cities_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df = pd.read_csv(filepath, index_col=False)
    city_column = df['City'].copy()
    region_column = df['Region'].copy()

    df = dh.drop_columns(df, ['Region', 'City', '2006','2007','2008','2009','2011','2012','2013','2014'])

    combined_df = _split_dataframe_and_transpose(df, 17)

    combined_df.to_csv(filepath, header = False)

    df = pd.read_csv(filepath)

    df = dh.drop_columns(df, ['per person, tCO2e', 'F-gases', 'Emission credits'])

    city_column = dh.remove_extra_rows_from_not_unique_series(city_column, 11)
    region_column = dh.remove_extra_rows_from_unique_series(region_column, 11)
    df['City'] = city_column
    df['Region'] = region_column

    df = dh.rename_columns(df)
    
    df['Region'] = df['Region'].apply(dh.replace_special_chars)
    df['Region'] = df['Region'].apply(dh.replace_word_to_camel_case)
    df['City'] = df['City'].apply(dh.replace_special_chars)
    df['City'] = df['City'].apply(dh.replace_word_to_camel_case)

    df.to_csv(filepath, index=False)

def _transform_regions_data() -> None:
    # Removing bad headers and rows in regions files
    _removing_headers_and_bad_rows()

    # Making it into one file - all regions to one file
    _make_custom_csv_file()

    # This is where i turned the dataframes around - making the columns become rows and rows become columns
    _remove_columns_not_needed_and_flip_columns_and_rows()
    # Cleaning more data, renaming columns, adding them together and setting the correct order of the dataframe
    _renaming_columns_and_adding_columns_together()

def _renaming_columns_and_adding_columns_together() -> None:
    filename = 'finland_regions_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df = pd.read_csv(filepath, index_col=False)
    
    df = dh.rename_columns(df)
    df['Region'] = df['Region'].apply(dh.replace_special_chars)
    df['Region'] = df['Region'].apply(dh.replace_word_to_camel_case)

    filename = 'finland_regions_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df.to_csv(filepath, index=False)

def _split_dataframe_and_transpose(df: pd.DataFrame, chunk_size: int) -> pd.DataFrame:

    dfs = [df.iloc[i:i + chunk_size].reset_index(drop=True) for i in range(0, len(df), chunk_size)]
    
    df_combined = dfs[0]
    df_combined.set_index('Hinku calculation without emission credits', inplace=True)
        
    for df in dfs[1:]:
        df.set_index('Hinku calculation without emission credits', inplace=True)
        
        df_combined = pd.concat([df_combined, df], axis=1)
            
    df_combined.reset_index(inplace=True)    
    df_combined = df_combined.transpose()

    return df_combined

def _remove_columns_not_needed_and_flip_columns_and_rows() -> None:
    filename = 'finland_regions_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df = pd.read_csv(filepath, index_col=False)
    df_cleaned = df[df['Hinku calculation without emission credits'] != 'F-gases']
    df_cleaned = df_cleaned[df_cleaned['Hinku calculation without emission credits'] != 'Emission credits']
    df_cleaned = df_cleaned[df_cleaned['Hinku calculation without emission credits'] != 'per person. tCO2e']
    df_cleaned.drop(columns=['2006','2007','2008','2009','2011','2012','2013','2014'], axis=1, inplace=True)
    region_column = df_cleaned['Region'].copy()
    df_cleaned.drop(columns=['Region'], axis=1, inplace=True)
    
    df_combined = _split_dataframe_and_transpose(df_cleaned, 14)
    
    df_combined.to_csv(filepath)

    # Flipping rows and columns and adding region back
    df = pd.read_csv(filepath, header = 1)
    
    result_series = dh.remove_extra_rows_from_unique_series(region_column, 11)

    df['Region'] = result_series

    df.to_csv(filepath, index=False)

def _remove_nan_from_csv_file() -> None:
    filename = 'finland_regions_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df = pd.read_csv(filepath)
    print(df.isna().sum())
    df.fillna(0, inplace=True)
    df.to_csv(filepath, index=False)

def _make_custom_csv_file() -> None:
    custom_csv_filename = 'finland_regions_emissions.csv'
    filepath_output = fh.get_path_of_folder('transformed_finland_data')
    filepath = fh.get_path_of_folder('transformed_finland_data/regions')
    list_with_files = fh.get_list_with_names_from_folder(filepath)

    split_word = 'Hinku'

    output_df = pd.DataFrame()

    for file in list_with_files:
        filepath_of_file = os.path.join(filepath, file)
        df = pd.read_csv(filepath_of_file, header = 1)
        first_column = df.columns[0]
        region, column_name = first_column.split(split_word)
        column_name = split_word + column_name
        df.rename(columns={first_column: column_name}, inplace=True)
        df['Region'] = region
        output_df = pd.concat([output_df, df])
        
    file_output = os.path.join(filepath_output, custom_csv_filename)
    output_df.to_csv(file_output, index=False)

def _removing_headers_and_bad_rows() -> None:
    # Taking files from finland_data making it a list, then writing them to csv files to folder transformed_finland_data
    folder_name_input = 'finland_data/regions'
    folder_name_output = 'transformed_finland_data/regions'
    filepath_output = fh.get_path_of_folder(folder_name_output)
    filepath_input = fh.get_path_of_folder(folder_name_input)
    list_with_files_input = fh.get_list_with_names_from_folder(filepath_input)
    list_with_files_output = fh.get_list_with_names_from_folder(filepath_output)
    convert.convert_list_with_files(list_with_files_input, filepath_input, filepath_output)
    
    
    # Removing headers and bad rows
    for file in list_with_files_output:
        filepath_of_file = os.path.join(filepath_output, file)
        df = pd.read_csv(filepath_of_file, header=0)
        df.to_csv(filepath_of_file, header=False, index=False)

        df = pd.read_csv(filepath_of_file, header=0)
        column_to_drop = df.columns[0]
        df.drop(columns=[column_to_drop], inplace=True)
        df.to_csv(filepath_of_file, index=False)

    dh.change_values_in_multiple_files(filepath_output, list_with_files_output, ',', '.')
 
if __name__ == "__main__":
    main()