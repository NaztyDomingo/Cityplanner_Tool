import pandas as pd




def drop_columns_for_cities(data: pd.DataFrame) -> pd.DataFrame:
    
    data = data.drop(columns=['Subsector', 'CO2 2000'])
    data = data.reset_index(drop=True)

    return data

def drop_columns_for_regions(data: pd.DataFrame) -> pd.DataFrame:
    
    data = data.drop(columns=['Subsector','City', 'CO2 2000'])
    data = data.reset_index(drop=True)

    return data


def drop_rows_for_cities(data: pd.DataFrame) -> pd.DataFrame:
    # Keep rows where 'Subsector' is 'Alla'
    data = data[data['Subsector'] == 'Alla']

    # Drop rows where 'Main sector' is 'Alla', 'Product Use', or 'Exportation'
    data = data[~data['Main sector'].isin(['Alla', 'Product Use', 'Exportation'])]

    # Drop rows where 'Region' or 'City' is 'Alla' for emissions by cities 
    data = data[(data['Region'] != 'Alla') & (data['City'] != 'Alla')]

    # Reset index after all filtering
    data = data.reset_index(drop=True)

    return data

def drop_rows_for_regions(data: pd.DataFrame) -> pd.DataFrame:
    # Keep rows where 'Subsector' is 'Alla'
    data = data[data['Subsector'] == 'Alla']

    # Drop rows where 'Main sector' is 'Alla', 'Product Use', or 'Exportation'
    data = data[~data['Main sector'].isin(['Alla', 'Product Use', 'Exportation'])]

    # Drop rows where 'Region' or 'City' is 'Alla' for emissions by cities 
    data = data[(data['Region'] != 'Alla') & (data['City'] == 'Alla')]

    # Reset index after all filtering
    data = data.reset_index(drop=True)

    return data


def replace_special_characters(text: str) -> str:
    text = text.replace('å', 'aa')
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    text = text.replace('Å', 'Aa')
    text = text.replace('Ä', 'Ae')
    text = text.replace('Ö', 'Oe')
    return text


def translate_replace(data: pd.DataFrame) -> pd.DataFrame:
    header_translation = {
        'Huvudsektor': 'Main sector',
        'Undersektor': 'Subsector',
        'Län': 'Region',
        'Kommun': 'City'
    }

    value_translation = {
        'Main sector':{
            'Transporter':'Transportation',
            'Industri (energi + processer)':'Industry',
            'Jordbruk':'Agriculture',
            'El och fjärrvärme':'Electricity And District Heating',
            'Egen uppärmning av bostäder och lokaler':'Other Heating',
            'Arbetsmaskiner':'Machinery',
            'Produktanvändning (inkl. lösningsmedel)':'Product Use',
            'Avfall (inkl.avlopp)':'Waste And Sewage',
            'Utrikes transporter':'Exportation'
            
        }}
    
    #Translate column headers
    translated_headers = {key: header_translation.get(value, value) for key, value in data.columns.to_series().items()}
    data = data.rename(columns=translated_headers)

    #translate every sector in main sector
    for col in ['Main sector']:
        if col in data.columns:
            data[col] = data[col].map(value_translation[col]).fillna(data[col])

    #Replace special characters in region and city values
    data['Region'] = data['Region'].apply(replace_special_characters)
    data['City'] = data['City'].apply(replace_special_characters)
    
    return data


def transform_city_data(data: pd.DataFrame) -> pd.DataFrame:
    data_melted = data.melt(id_vars=['Main sector', 'Region', 'City'], 
                            var_name='Year', 
                            value_name='Emission')
    
    data_melted['Year'] = data_melted['Year'].str.extract(r'(\d{4})').astype(int)
    
    data_melted['Emission'] = data_melted['Emission'] / 1000

    data_pivoted = data_melted.pivot_table(index=['Year', 'City', 'Region'], 
                                           columns='Main sector', 
                                           values='Emission', 
                                           aggfunc='sum').reset_index()
    for sector in ['Transportation', 'Industry','Agriculture', 'Electricity And District Heating', 'Other Heating', 'Machinery', 'Waste And Sewage']:
        if sector not in data_pivoted:
            data_pivoted[sector] = 0
    
    data_pivoted['Total Emissions'] = data_pivoted[['Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                                                   'Other Heating', 'Agriculture', 'Transportation', 'Industry']].sum(axis=1)
    data_pivoted['Population'] = 0

    final_columns = ['Year', 'City', 'Region', 'Population', 'Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                     'Other Heating', 'Agriculture', 'Transportation', 'Industry', 'Total Emissions']
    data_pivoted = data_pivoted[final_columns]
    
    return data_pivoted

def transform_region_data(data: pd.DataFrame) -> pd.DataFrame:
    data_melted = data.melt(id_vars=['Main sector', 'Region'], 
                            var_name='Year', 
                            value_name='Emission')
    
    data_melted['Year'] = data_melted['Year'].str.extract(r'(\d{4})').astype(int)
    
    data_melted['Emission'] = data_melted['Emission'] / 1000

    data_pivoted = data_melted.pivot_table(index=['Year', 'Region'], 
                                           columns='Main sector', 
                                           values='Emission', 
                                           aggfunc='sum').reset_index()
    for sector in ['Transportation', 'Industry','Agriculture', 'Electricity And District Heating', 'Other Heating', 'Machinery', 'Waste And Sewage']:
        if sector not in data_pivoted:
            data_pivoted[sector] = 0
    
    data_pivoted['Total Emissions'] = data_pivoted[['Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                                                   'Other Heating', 'Agriculture', 'Transportation', 'Industry']].sum(axis=1)
    data_pivoted['Population'] = 0

    final_columns = ['Year','Region', 'Population', 'Waste And Sewage', 'Machinery', 'Electricity And District Heating', 
                     'Other Heating', 'Agriculture', 'Transportation', 'Industry', 'Total Emissions']
    data_pivoted = data_pivoted[final_columns]
    
    return data_pivoted

