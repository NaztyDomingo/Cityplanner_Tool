import filehandler_helper as fh
import os
import pandas as pd

# For loading data and serving resulting dataframes for visualization purposes in Dash
def load_data():

    # Read csv files to get data
    # Finland dataframes
    filepath = fh.get_path_of_folder('transformed_finland_data')
    filepath_of_fin_cities = os.path.join(filepath, 'finland_cities_emissions.csv')
    filepath_of_fin_regions = os.path.join(filepath, 'finland_regions_emissions.csv')
    fin_cities_df = pd.read_csv(filepath_of_fin_cities)
    fin_regions_df = pd.read_csv(filepath_of_fin_regions)

    # TODO:
    # Sweden dataframes
    # Get Sweden city data
    # Get Sweden region data

    # Combine SWE+FIN city data
    # Combine SWE+FIN region data ?

    # Tree dataframe
    filepath = fh.get_path_of_folder('transformed_tree_data')
    filepath_of_trees = os.path.join(filepath, 'final_tree_info.csv')
    tree_df = pd.read_csv(filepath_of_trees)

    # Return all dfs
    list_of_dfs = [fin_cities_df, fin_regions_df, tree_df]
    return list_of_dfs