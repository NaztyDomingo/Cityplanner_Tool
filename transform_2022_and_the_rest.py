import pandas as pd 
import transform as t
import read_data as rd
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emission_all_regions_2022.csv'))
# output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_2022.csv')

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emissions_region.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_all.csv')

data = rd.read_file(file_path)

# data = t.converter(data)

# data = t.drop_row(data)

data = t.drop_columns(data)

# data = t.transform_columns(data)

data = t.rename_reorder_columns(data)

t.data_to_csv(data)