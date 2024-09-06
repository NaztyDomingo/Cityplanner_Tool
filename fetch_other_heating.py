import pandas as pd
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'sweden_cities_emissions.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'other_heating.csv')

def fetch_heating(data: pd.DataFrame) ->pd.DataFrame:
    df_22 = data[data['Year'] == 2022]

    grouped_df = df_22.groupby('Region', as_index=False)['Other Heating'].sum()

    grouped_df['Other Heating'] = grouped_df['Other Heating'].round(1)

    grouped_df['Year'] = 2022

    grouped_df = grouped_df[['Region', 'Year', 'Other Heating']]

    return grouped_df

data = pd.read_csv(file_path)

data = fetch_heating(data) 

data.to_csv(output_file, index=False)
