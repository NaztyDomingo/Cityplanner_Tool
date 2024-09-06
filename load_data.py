from sqlalchemy import create_engine
import pandas as pd
import configparser
import filehandler_helper as fh
import psycopg2

def main() -> None:
    db_name = 'cityplanner_db'
    db_username, db_password = _get_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    conn = _establish_connection(db_username, db_password, db_name)
    _create_table('test_tiril', conn)


def _get_username_and_password(section_name: str, username_label: str, password_label: str) -> tuple[str, str]:
    config = configparser.ConfigParser()
    config_filename = 'config.ini'
    filepath = fh.return_filepath_joined_with_file(fh.get_current_filepath(), config_filename)
    config.read(filepath)
    db_username = config.get(section_name, username_label)
    db_password = config.get(section_name, password_label)
    return db_username, db_password

def _establish_connection(db_username: str, db_password: str, db_name: str, port_number : int = 5432, hostname : str = 'localhost') -> psycopg2.connect:
    conn = psycopg2.connect(database = db_name, 
                            user = db_username,
                            host = hostname,
                            password = db_password,
                            port = port_number)
    return conn

def _create_table(table_name: str, connection_instance: psycopg2.connect) -> None:
    cur = connection_instance.cursor()

    cur.execute(f"""CREATE TABLE {table_name}(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
                )""")
    
    connection_instance.commit()
    cur.close()
    connection_instance.close()

if __name__ == "__main__":
    main()