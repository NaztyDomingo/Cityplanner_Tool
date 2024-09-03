import filehandler_helper as fh
import xlsx_to_csv_converter as convert
import pandas as pd
import os

def main() -> None:
    #convert.convert_single_file('finland_data', 'transformed_finland_data', 'finland_cities_emissions')
    #_removing_headers_and_bad_rows()
    #_change_values()

    # Making it into one file - all regions to one file
    #_make_custom_csv_file()
    #_remove_nan_from_csv_file()
    print('All files transformed...')

def _remove_nan_from_csv_file() -> None:
    filename = 'finland_regions_emissions.csv'
    folder = 'transformed_finland_data'
    filepath = fh.get_path_of_file(folder, filename)
    df = pd.read_csv(filepath)
    df.fillna(0, inplace=True)
    print(df.isna().sum())
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
        df = pd.read_csv(filepath_of_file)
        first_column = df.columns[0]
        region, column_name = first_column.split(split_word)
        column_name = split_word + column_name
        df.rename(columns={first_column: column_name}, inplace=True)
        df['Region'] = region
        output_df = pd.concat([output_df, df])
        
    file_output = os.path.join(filepath_output, custom_csv_filename)
    output_df.to_csv(file_output, index=False)

def _change_values() -> None:
    filepath = fh.get_path_of_folder('transformed_finland_data/regions')
    list_with_files = fh.get_list_with_names_from_folder(filepath)

    for file in list_with_files:
        filepath_of_file = os.path.join(filepath, file)
        df = pd.read_csv(filepath_of_file)
        for column in df.columns:
            df[column] = df[column].str.replace(',', '.')
        
        df.to_csv(filepath_of_file, index=False)

def _removing_headers_and_bad_rows() -> None:
    # Taking files from finland_data making it a list, then writing them to csv files to folder transformed_finland_data
    folder_name_input = 'finland_data/regions'
    folder_name_output = 'transformed_finland_data/regions'
    convert.convert_list_with_files(fh.get_list_with_names_from_folder(fh.get_path_of_folder(folder_name_input)), fh.get_path_of_folder(folder_name_input), fh.get_path_of_folder(folder_name_output))
    filepath = fh.get_path_of_folder(folder_name_output)
    list_with_files = fh.get_list_with_names_from_folder(filepath)
    
    # Removing headers and bad rows
    for file in list_with_files:
        filepath_of_file = os.path.join(filepath, file)
        df = pd.read_csv(filepath_of_file, header=0)
        df.to_csv(filepath_of_file, header=False, index=False)

        df = pd.read_csv(filepath_of_file, header=0)
        column_to_drop = df.columns[0]
        df.drop(columns=[column_to_drop], inplace=True)
        df.to_csv(filepath_of_file, index=False)

if __name__ == "__main__":
    main()