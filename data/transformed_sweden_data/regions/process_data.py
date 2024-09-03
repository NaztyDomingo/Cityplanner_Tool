import pandas as pd
import os
import glob
import read_data as rd
import translate_replace as tr
import transform as t

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_paths = glob.glob(os.path.join(CURR_DIR_PATH, '*.csv'))

output_file = os.path.join(CURR_DIR_PATH, 'emissions_by_region.csv')

def process_files(file_paths):
    all_transformed_data = []

    for file_path in file_paths:
        region = os.path.basename(file_path).split('.')[0]
        data = rd.read_file(file_path)
        data = tr.translate_replace(data)
        data['Region'] = region + ' County'

        print(f"Columns after translation for {region}: {data.columns.tolist()}")

        transformed_data = t.transform_data(data)
        all_transformed_data.append(transformed_data)

    processed_data = pd.concat(all_transformed_data, ignore_index=True)
    return processed_data

def combine_and_save(file_paths, output_file):
    combined_df = process_files(file_paths)
    combined_df.to_csv(output_file, index=False)
    print(combined_df.head())


combine_and_save(file_paths, output_file)