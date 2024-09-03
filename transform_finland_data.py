import filehandler_helper as fh
import xlsx_to_csv_converter as convert
import pandas as pd
import os

def main() -> None:
    # Taking files from finland_data making it a list, then writing them to csv files to folder transformed_finland_data
    convert.convert_list_with_files(fh.get_list_with_names_from_folder(fh.get_path_of_folder('finland_data')), fh.get_path_of_folder('finland_data'), fh.get_path_of_folder('transformed_finland_data'))
    filepath = fh.get_path_of_folder('transformed_finland_data')
    list_with_files = fh.get_list_with_names_from_folder(filepath)
    
    for file in list_with_files:
        filepath_of_file = os.path.join(filepath, file)
        df = pd.read_csv(filepath_of_file)
        df.drop([17], inplace=True)
        df.to_csv(filepath_of_file, header=False)

if __name__ == "__main__":
    main()