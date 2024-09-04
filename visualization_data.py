import filehandler_helper as fh
import os
import pandas as pd

# For loading data and serving resulting dataframes for visualization purposes in Dash
def load_data():
    
    # Read csv files to get data
    # Finland data
    filepath = fh.get_path_of_folder('transformed_finland_data')
    filepath_of_fin_cities = os.path.join(filepath, 'finland_cities_emissions.csv')
    filepath_of_fin_regions = os.path.join(filepath, 'finland_regions_emissions.csv')
    fin_cities_df = pd.read_csv(filepath_of_fin_cities)
    fin_regions_df = pd.read_csv(filepath_of_fin_regions)

    # Sweden data
    # TBA

    # Combine SWE+FIN city data
    # Combine SWE+FIN region data ?

    # Tree data
    filepath = fh.get_path_of_folder('transformed_tree_data')
    filepath_of_trees = os.path.join(filepath, 'final_tree_info.csv')
    tree_df = pd.read_csv(filepath_of_trees)

    # Dash example:
    df = pd.DataFrame({
        'Category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'],
        'Variable': ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z'],
        'Values': [4, 3, 6, 1, 5, 7, 2, 8, 5, 5, 7, 6]
    })

    list_of_dfs = [fin_cities_df, fin_regions_df, tree_df, df]
    return list_of_dfs