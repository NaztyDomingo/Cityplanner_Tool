import load_data

def pull_all() -> list:
    db_name = load_data.get_db_name()
    db_user, db_pass = load_data.get_db_username_and_password('DEV', 'cityplanner_db_username', 'cityplanner_db_password')
    lst = load_data.pull_all_tables_return_list_with_dfs(db_user, db_pass, db_name)
    return lst