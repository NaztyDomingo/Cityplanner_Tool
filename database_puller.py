import load_data
import pandas as pd

def pull_all() -> list:
    db_name = load_data.get_db_name()
    db_user, db_pass = load_data.get_db_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    lst = load_data.pull_all_tables_return_list_with_dfs(db_user, db_pass, db_name)
    return lst

def pull_predictions(city: str) -> pd.DataFrame:
    db_name = load_data.get_db_name()
    db_user, db_pass = load_data.get_db_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    df = load_data.pull_prediction_data_from_city(city, db_user, db_pass, db_name)
    return df