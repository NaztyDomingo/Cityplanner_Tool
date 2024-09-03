import pandas as pd
import os
import glob

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_paths = glob.glob(os.path.join(CURR_DIR_PATH, '*.csv'))

output_file = os.path.join(CURR_DIR_PATH, 'combined_emissions.csv')

# Header translation dictionary
header_translation = {
    'År': 'Year',
    'Produktanvändning (inkl. lösningsmedel)': 'Product Use',
    'Avfall (inkl. avlopp)': 'Waste and Sewage',
    'Arbetsmaskiner': 'Machinery',
    'Egen uppvärmning av bostäder <br>och lokaler': 'Heating',
    'El och fjärrvärme': 'Electricity and District Heating',
    'Jordbruk': 'Agriculture',
    'Inrikes transporter': 'Transportation',
    'Industri (energi och processer)': 'Industry'
}

def read_file(file_path):
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    return data

def replace_special_characters(text):
    text = text.replace('å', 'aa')
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    return text

def translate_replace(data):
   
    translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    data = data.rename(columns=translated_headers)
    
    data.columns = [replace_special_characters(col) for col in data.columns]
    
    return data

def transform_data(data, region):
    print(f"Columns available in transform_data: {data.columns.tolist()}")

    try:
        data['Total Emissions'] = data.loc[:, 'Electricity and District Heating':'Waste and Sewage'].sum(axis=1)
    except KeyError as e:
        print(f"Column error: {e}")
        raise

    data['Region'] = region + ' County'
    
    return data

def process_files(file_paths):
    all_transformed_data = []

    for file_path in file_paths:
        region = os.path.basename(file_path).split('.')[0]
        data = read_file(file_path)
        data = translate_replace(data)

        print(f"Columns after translation for {region}: {data.columns.tolist()}")

        transformed_data = transform_data(data, region)
        all_transformed_data.append(transformed_data)

    processed_data = pd.concat(all_transformed_data, ignore_index=True)
    return processed_data

def combine_and_save(file_paths, output_file):
    combined_df = process_files(file_paths)
    combined_df.to_csv(output_file, index=False)
    print(combined_df.head())


combine_and_save(file_paths, output_file)
