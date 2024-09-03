header_translation = {
    'År': 'Year',
    'Produktanvändning (inkl. lösningsmedel)': 'Product Use',
    'Avfall (inkl. avlopp)': 'Waste and Sewage',
    'Arbetsmaskiner': 'Machinery',
    'Egen uppvärmning av bostäder <br>och lokaler': 'Heating',
    'El och fjärrvärme': 'Electricity and District_Heating',
    'Jordbruk': 'Agriculture',
    'Inrikes transporter': 'Transportation',
    'Industri (energi och processer)': 'Industry'
}

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