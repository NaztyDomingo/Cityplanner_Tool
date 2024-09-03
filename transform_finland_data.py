import filehandler_helper as fh
import xlsx_to_csv_converter as convert

def main() -> None:
    convert.convert_list_with_files(fh.get_list_with_names_from_folder(fh.get_path_of_folder('finland_data')), fh.get_path_of_folder('finland_data'), fh.get_path_of_folder('transformed_finland_data'))

if __name__ == "__main__":
    main()