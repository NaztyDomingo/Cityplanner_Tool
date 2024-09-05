import pandas as pd
import glob
import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# # file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emission_all_regions_2022.csv'))[0]
# # output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_2022.csv')

# file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'emissions_region.csv'))[0]
# output_file = os.path.join(CURR_DIR_PATH, 'emissions_region_all.csv')

# output_file = os.path.join(CURR_DIR_PATH, 'city_emission_dirty.csv')
output_file = os.path.join(CURR_DIR_PATH, 'city_emission.csv')


def converter(data: pd.DataFrame) -> pd.DataFrame:
    data['Population'] = data['Population'].str.replace(' ', '').astype(int)
    data['Total'] = data['Total'].str.replace(' ', '').astype(int)
    data['Total Emissions'] = (data['Total'] * data['Population']) / 1_000_000
    return data

def drop_columns(data: pd.DataFrame) -> pd.DataFrame:
    # data = data.drop(columns=['Total', 'Product_use'])
    # data = data.drop(columns=['Product Use'])
    # data = data.reset_index(drop=True)
    data = data.drop(columns=['Subsector', 'CO2 2000'])
    data = data.reset_index(drop=True)

    return data

def drop_row(data: pd.DataFrame) -> pd.DataFrame:
    # data = data[data['Regions'] != 'Country of Sweden']
    # data = data.reset_index(drop=True)

    # data = data[data['Subsector'] == 'Alla']
    # data = data.reset_index(drop=True)
    
    # data = data[data['Main sector'] != 'Alla']
    # data = data.reset_index(drop=True)
    
    data = data[data['County'] != 'Alla']
    data = data.reset_index(drop=True)
    
    data = data[data['Municipality'] != 'Alla']
    data = data.reset_index(drop=True)

    data = data[data['Main sector'] != 'Produktanvändning (inkl. lösningsmedel)']
    data = data.reset_index(drop=True)

    data = data[data['Main sector'] != 'Utrikes transporter']
    data = data.reset_index(drop=True)

    return data

def transform_columns(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = data.columns.str.replace('_', ' ').str.title()
    return data

# def transform_data(data: pd.DataFrame) -> pd.DataFrame:
#     data['Total Emissions'] = data[['Heating', 'Electricity and District Heating', 'Industry', 
#                                     'Transportation', 'Machinery', 'Product Use', 'Agriculture', 
#                                     'Waste and Sewage']].sum(axis=1)
#     return data

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

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    data_melted = data.melt(id_vars=['Main sector', 'County', 'Municipality'], 
                            var_name='Year', 
                            value_name='Emission')
    
    data_melted['Year'] = data_melted['Year'].str.extract('(\d{4})').astype(int)
    
    data_melted = data_melted.rename(columns={'County': 'Region', 'Municipality': 'City'})
    
    data_melted['Emission'] = data_melted['Emission'] / 1000

    data_pivoted = data_melted.pivot_table(index=['Year', 'City', 'Region'], 
                                           columns='Main sector', 
                                           values='Emission', 
                                           aggfunc='sum').reset_index()
    for sector in ['Waste And Sewage', 'Machinery', 'Electricity And District Heating', 'Other Heating', 'Agriculture', 'Transportation', 'Industry']:
        if sector not in data_pivoted:
            data_pivoted[sector] = 0
    
    data_pivoted['Total Emission'] = data_pivoted[['Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                                                   'Other Heating', 'Agriculture', 'Transportation', 'Industry']].sum(axis=1)
    data_pivoted['Population'] = 0

    final_columns = ['Year', 'City', 'Region', 'Population', 'Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                     'Other Heating', 'Agriculture', 'Transportation', 'Industry', 'Total Emission']
    data_pivoted = data_pivoted[final_columns]
    
    return data_pivoted

def data_to_csv(data: pd.DataFrame) -> None:
    data.to_csv(output_file, index=False)


