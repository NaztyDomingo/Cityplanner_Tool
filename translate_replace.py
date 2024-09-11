import pandas as pd

header_translation = {
    'År': 'Year',
    'Produktanvändning (inkl. lösningsmedel)': 'Product Use',
    'Avfall (inkl. avlopp)': 'Waste and Sewage',
    'Arbetsmaskiner': 'Machinery',
    'Egen uppvärmning av bostäder och lokaler': 'Heating',
    'El och fjärrvärme': 'Electricity and District Heating',
    'Jordbruk': 'Agriculture',
    'Inrikes transporter': 'Transportation',
    'Industri (energi och processer)': 'Industry'
}


def replace_special_characters(text: str) -> str:
    text = text.replace('å', 'aa')
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    text = text.replace('Å', 'AA')
    text = text.replace('Ä', 'AE')
    text = text.replace('Ö', 'OE')
    return text


def translate_replace(data: pd.DataFrame) -> pd.DataFrame:
    header_translation = {
        'Huvudsektor': 'Main sector',
        'Undersektor': 'Subsector',
        'Län': 'County',
        'Kommun': 'Municipality'
    }

    value_translation = {
        'Main sector':{
            'Arbetsmaskiner':'Machinery',
            'Avfall (inkl.avlopp)':'Waste And Sewage',
            'Egen uppärmning av bostäder och lokaler':'Other Heating',
            'El och fjärrvärme':'Electricity And District Heating',
            'Industri (energi + processer)':'Industry',
            'Transporter':'Transportation'
        }}
    
    translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    data = data.rename(columns=translated_headers)
    
    data.columns = [replace_special_characters(col) for col in data.columns]

    translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    data = data.rename(columns=translated_headers)
    

    for col in ['Main sector']:
        if col in data.columns:
            data[col] = data[col].map(value_translation[col]).fillna(data[col])

    data['County'] = data['County'].apply(replace_special_characters)
    data['Municipality'] = data['Municipality'].apply(replace_special_characters)
    
    return data
