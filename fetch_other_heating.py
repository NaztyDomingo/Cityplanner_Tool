import filter_and_save as fs 
import read_data as rd
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'county_city_emissions.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'other_heating.csv')

data = rd.read_file(file_path)

fetched_data = fs.calculate_heating(data)

fetched_data.to_csv(output_file, index=False)
