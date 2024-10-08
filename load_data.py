from sqlalchemy import create_engine
import pandas as pd
import configparser
import filehandler_helper as fh
import psycopg2
import dataframe_helper as dh

def main() -> None:
    db_username, db_password = get_db_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    to_database(db_username, db_password, get_db_name())

def get_db_name() -> str:
    return 'cityplanner_db'

def get_db_username_and_password(section_name: str, username_label: str, password_label: str) -> tuple[str, str]:
    config = configparser.ConfigParser()
    config_filename = 'config.ini'
    filepath = fh.return_filepath_joined_with_file(fh.get_current_filepath(), config_filename)
    config.read(filepath)
    db_username = config.get(section_name, username_label)
    db_password = config.get(section_name, password_label)
    return db_username, db_password

def establish_connection(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> psycopg2.connect:
    return psycopg2.connect(database = db_name, 
                            user = db_username,
                            host = hostname,
                            password = db_password,
                            port = port_number)

def _create_engine(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> create_engine:
    postgres_engine = create_engine(
        f'postgresql+psycopg2://{db_username}:{db_password}@{hostname}:{port_number}/{db_name}'
    )   
    return postgres_engine

def to_database(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> None:
    filepath = fh.get_path_of_folder('')
    list_with_folder_names = fh.search_folder_get_list_with_foldernames('transformed_', filepath)
    list_with_files_to_load = fh.get_tupled_list_with_filename_and_filepath_from_list_with_folder_names(list_with_folder_names)

    for filename, filepath in list_with_files_to_load:
        df = pd.read_csv(filepath)

        engine = _create_engine(db_username, db_password, db_name, port_number, hostname)

        df.to_sql(name = filename, con = engine, if_exists ='replace', index=False)

def select_table(table_name: str, engine: create_engine, select_input: str = '*') -> pd.DataFrame:
    df = pd.read_sql_query(f'SELECT {select_input} FROM {table_name}', con=engine)
    return df

def pull_all_tables_return_list_with_dfs(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> None:
    filepath = fh.get_path_of_folder('')
    list_with_folder_names = fh.search_folder_get_list_with_foldernames_without_predictions('transformed_', filepath)
    list_with_files_to_load = fh.get_tupled_list_with_filename_and_filepath_from_list_with_folder_names(list_with_folder_names)

    engine = _create_engine(db_username, db_password, db_name, port_number, hostname)
    list_with_dfs = []
    for filename, filepath in list_with_files_to_load:
        list_with_dfs.append(select_table(filename, engine))

    return list_with_dfs

def pull_prediction_data_from_city(city: str, db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> pd.DataFrame:
    engine = _create_engine(db_username, db_password, db_name, port_number, hostname)

    city = dh.replace_special_chars(city)
    print(city)
    table_name = 'sweden_city_predictions'
    try:
        prediction_df = pd.read_sql_query(f'SELECT "Year", "{city.capitalize()}" FROM {table_name}', con=engine)
    except:
        table_name = 'finland_city_predictions'
        prediction_df = pd.read_sql_query(f'SELECT "Year", "{city.capitalize()}" FROM {table_name}', con=engine)

    return prediction_df
    


if __name__ == "__main__":
    main()