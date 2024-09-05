import pandas as pd
# import glob
# import os

# CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# # file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emission_all_regions_2022.csv'))[0]
# # output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_2022.csv')

# file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emissions_region.csv'))[0]
# output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_all.csv')

def converter(data: pd.DataFrame) -> pd.DataFrame:
    data['Population'] = data['Population'].str.replace(' ', '').astype(int)
    data['Total'] = data['Total'].str.replace(' ', '').astype(int)
    data['Total Emissions'] = (data['Total'] * data['Population']) / 1_000_000
    return data

def drop_columns(data: pd.DataFrame) -> pd.DataFrame:
    # data = data.drop(columns=['Total', 'Product_use'])
    data = data.drop(columns=['Product Use'])
    data = data.reset_index(drop=True)
    return data

def drop_row(data: pd.DataFrame) -> pd.DataFrame:
    # data = data[data['Regions'] != 'Country of Sweden']
    # data = data.reset_index(drop=True)

    data = data[data['Subsector'] == 'Alla']
    data = data.reset_index(drop=True)
    
    data = data[data['Main sector'] != 'Alla']
    data = data.reset_index(drop=True)
    
    return data

def transform_columns(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = data.columns.str.replace('_', ' ').str.title()
    return data

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    data['Total Emissions'] = data[['Heating', 'Electricity and District Heating', 'Industry', 
                                    'Transportation', 'Machinery', 'Product Use', 'Agriculture', 
                                    'Waste and Sewage']].sum(axis=1)
    return data

def rename_reorder_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.rename(columns={
        'Regions': 'Region',
        'Electricity and District Heating': 'Electricity And District Heating',
        'Heating':'Other Heating',
        'Waste and Sewage': 'Waste And Sewage',
        'Total': 'Total Emissions'
    })
    
    data['Population'] = 'NaN'
    
    new_order = [
        'Year',
        'Region',
        'Population',
        'Waste And Sewage',
        'Machinery',
        'Electricity And District Heating',
        'Other Heating',
        'Agriculture',
        'Transportation',
        'Industry',
        'Total Emissions'
    ]
    
    data = data[new_order]
    
    return data

def data_to_csv(data: pd.DataFrame) -> None:
    data.to_csv(output_file, index=False)


