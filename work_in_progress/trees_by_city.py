import pandas as pd
import read_data as rd
import transform as t
import glob 
import os

#defining current directory
CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

#defining path to csv files with datasets needed
file_path_1 = glob.glob(os.path.join(CURR_DIR_PATH, 'sweden_cities_emissions.csv'))[0]
file_path_2 = glob.glob(os.path.join(CURR_DIR_PATH, 'final_tree_info.csv'))[0]

#Creating city dataframe
data = rd.read_file(file_path_1)
#Creating tree dataframe
tree_df = rd.read_file(file_path_2)

print(data)
#Filter city dataframe to only contain cities and total emissions
data = t.drop_columns(data)
#Filter dataframe to only contain data from 2022
print(data)

data = t.drop_row(data)

print(data)
