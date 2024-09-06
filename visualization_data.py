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
    filepath = fh.get_path_of_folder('transformed_sweden_data')
    filepath_of_swe_cities = os.path.join(filepath, 'sweden_cities_emissions.csv')
    filepath_of_swe_regions = os.path.join(filepath, 'sweden_regions_emissions.csv')
    swe_cities_df = pd.read_csv(filepath_of_swe_cities)
    swe_regions_df = pd.read_csv(filepath_of_swe_regions)

    # TODO: Combine SWE+FIN data
    #combine_cities = [fin_cities_df, swe_cities_df]
    #combined_cities_df = pd.concat(combine_cities)
    #combine_regions = [fin_regions_df, swe_regions_df]
    #combined_regions_df = pd.concat(combine_regions)
    # TODO: remember to add these dfs to the return list: combined_cities_df, combined_regions_df

    # Tree dataframe
    filepath = fh.get_path_of_folder('transformed_tree_data')
    filepath_of_trees = os.path.join(filepath, 'final_tree_info.csv')
    tree_df = pd.read_csv(filepath_of_trees)

    # Return all dfs
    list_of_dfs = [fin_cities_df, fin_regions_df, swe_cities_df, swe_regions_df, tree_df]
    return list_of_dfs