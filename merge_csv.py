import pandas as pd
import glob
import os


CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# file_path_1 = glob.glob(os.path.join(CURR_DIR_PATH, 'emissions_region_2022.csv'))[0]
# file_path_2 = glob.glob(os.path.join(CURR_DIR_PATH, 'emissions_region_all.csv'))[0]
# output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_90-22.csv')



file_path_1 = glob.glob(os.path.join(CURR_DIR_PATH, 'sweden_region_emissions.csv'))[0]
file_path_2 = glob.glob(os.path.join(CURR_DIR_PATH, 'other_heating.csv'))[0]
output_file = os.path.join(CURR_DIR_PATH, 'sweden_region_emission.csv')
# def merge_csv(file_path_1: str, file_path_2: str, output_file: str) -> None:

#     df1 = pd.read_csv(file_path_1)
#     df2 = pd.read_csv(file_path_2)

#     df2['Region'] = df2['Region'].str.title()
    
#     merged_df = pd.concat([df1, df2], ignore_index=True)
    
#     merged_df = merged_df.sort_values(by='Year').reset_index(drop=True)

#     merged_df.to_csv(output_file, index=False)

# merge_csv(file_path_1, file_path_2, output_file)

def merge_csv(file_path_1: str, file_path_2: str, output_file: str) -> None:

    df1 = pd.read_csv(file_path_1)
    df2 = pd.read_csv(file_path_2)

    df1.loc[df1['Year'] == 2022, 'Other Heating'] = df1.loc[df1['Year'] == 2022, 'Region'].map(df2.set_index('Region')['Other Heating'])
    
    # merged_df = df1.merge(df2, on=['Region', 'Year'], suffixes=('', '_new'))
    
    # merged_df['Other Heating'] = merged_df['Other Heating_new']
    
    # updated_df = merged_df.drop(columns=['Other Heating_new'])

    df1.to_csv(output_file, index=False)



merge_csv(file_path_1, file_path_2, output_file)