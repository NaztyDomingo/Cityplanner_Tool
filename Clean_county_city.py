import pandas as pd
import transform as t
import translate_replace as tr
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'county_city_emissions.csv'))[0]
# output_file = os.path.join(CURR_DIR_PATH, 'city_emission_dirty.csv')
file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'city_emission_dirty.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'city_emission.csv')

data = pd.read_csv(file_path)

data = t.drop_columns(data)

print(data)

data = t.drop_row(data)

print(data)

data = tr.translate_replace(data)

print(data)

data = t.transform_data(data)

t.data_to_csv(data)
