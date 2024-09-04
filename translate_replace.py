import pandas as pd

# header_translation = {
#     'År': 'Year',
#     'Produktanvändning (inkl. lösningsmedel)': 'Product Use',
#     'Avfall (inkl. avlopp)': 'Waste and Sewage',
#     'Arbetsmaskiner': 'Machinery',
#     'Egen uppvärmning av bostäder och lokaler': 'Heating',
#     'El och fjärrvärme': 'Electricity and District Heating',
#     'Jordbruk': 'Agriculture',
#     'Inrikes transporter': 'Transportation',
#     'Industri (energi och processer)': 'Industry'
# }


def replace_special_characters(text: str) -> str:
    text = text.replace('å', 'aa')
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    text = text.replace('Å', 'AA')
    text = text.replace('Ä', 'AE')
    text = text.replace('Ö', 'OE')
    return text

def replace_lan_with_county(text: str) -> str:
    return text.replace('laen', 'county')

def translate_replace(data: pd.DataFrame) -> pd.DataFrame:
   
    translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    data = data.rename(columns=translated_headers)
    
    data.columns = [replace_special_characters(col) for col in data.columns]
    
    return data

def rename_columns(data: pd.DataFrame) -> pd.DataFrame:

    data.rename(columns={
        'Unnamed: 0': 'Main sector',
        'Unnamed: 1': 'Subsector',
        'Unnamed: 2': 'County',
        'Unnamed: 3': 'Municipality'
    }, inplace=True)

    
    year_columns = data.columns[4:]  
    new_column_names = ['Total greenhouse gases in CO2-equivalent ' + str(year) for year in year_columns]
    data.columns = list(data.columns[:4]) + new_column_names

    data['County'] = data['County'].apply(replace_special_characters)
    data['Municipality'] = data['Municipality'].apply(replace_special_characters)

    data['County'] = data['County'].apply(replace_lan_with_county)

    return data

def drop_second_row(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(index=1)

    data = data.reset_index(drop=True)
    
    return data
