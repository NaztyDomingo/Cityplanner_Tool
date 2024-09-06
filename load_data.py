from sqlalchemy import create_engine
import pandas as pd
import configparser
import filehandler_helper as fh
import psycopg2

def main() -> None:
    db_username, db_password = get_db_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    _load_data(db_username, db_password, get_db_name)

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

def _create_table(table_name: str, connection_instance: psycopg2.connect) -> None:
    cur = connection_instance.cursor()

    cur.execute(f"""CREATE TABLE {table_name}(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
                )""")
    
    connection_instance.commit()
    cur.close()
    connection_instance.close()

def insert_table(df: pd.DataFrame, connection_instance: psycopg2.connect) -> None:
    cur = connection_instance.cursor()

    cur.execute(f"""INSERT INTO tiril_test (name) VALUES('Tiril')""")

    cur.commit()
    cur.close()
    connection_instance.close()

def to_database(df: pd.DataFrame, db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> None:
    engine = _create_engine(db_username, db_password, db_name, port_number, hostname)

    df.to_sql(name ='finland_regions_emissions', con = engine, if_exists ='replace', index=False)

def _load_data(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> None:
    folder_name = 'transformed_finland_data'
    filename = 'finland_regions_emissions.csv'
    filepath = fh.get_path_of_file(folder_name, filename)
    df = pd.read_csv(filepath)
    
    engine = _create_engine(db_username, db_password, db_name, port_number, hostname)

    df.to_sql(name ='finland_regions_emissions', con = engine, if_exists ='replace', index=False)


if __name__ == "__main__":
    main()