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


def translate_replace(data: pd.DataFrame) -> pd.DataFrame:
    header_translation = {
        'Huvudsektor': 'Main sector',
        'Undersektor': 'Subsector',
        'Län': 'County',
        'Kommun': 'Municipality'
    }

    value_translation = {
        'Main sector': {
            'Energisektor': 'Energy sector',
            'Industri': 'Industry',
            'Transport': 'Transport',
            'Jordbruk': 'Agriculture',
            'Avfall och avlopp': 'Waste and sewage',
            'Övrigt': 'Other'
        },
        'Subsector': {
            'Elektricitet och fjärrvärme': 'Electricity and district heating',
            'Tillverkning': 'Manufacturing',
            'Transportmedel': 'Transportation',
            'Boskap': 'Livestock',
            'Avfallshantering': 'Waste management'
        },
        'County': {
            'Blekinge län': 'Blekinge County',
            'Dalarnas län': 'Dalarna County',
            'Gotlands län': 'Gotland County',
            'Gävleborgs län': 'Gävleborg County',
            'Hallands län': 'Halland County',
            'Jämtlands län': 'Jämtland County',
            'Jönköpings län': 'Jönköping County',
            'Kalmar län': 'Kalmar County',
            'Kronobergs län': 'Kronoberg County',
            'Norrbottens län': 'Norrbotten County',
            'Skåne län': 'Skåne County',
            'Stockholms län': 'Stockholm County',
            'Södermanlands län': 'Södermanland County',
            'Uppsala län': 'Uppsala County',
            'Värmlands län': 'Värmland County',
            'Västerbottens län': 'Västerbotten County',
            'Västernorrlands län': 'Västernorrland County',
            'Västmanlands län': 'Västmanland County',
            'Västra Götalands län': 'Västra Götaland County',
            'Örebro län': 'Örebro County',
            'Östergötlands län': 'Östergötland County'
        }
    }
    # translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    # data = data.rename(columns=translated_headers)
    
    # data.columns = [replace_special_characters(col) for col in data.columns]

    translated_headers = {key: replace_special_characters(value) for key, value in header_translation.items()}
    data = data.rename(columns=translated_headers)
    

    for col in ['Main sector', 'Subsector', 'County']:
        if col in data.columns:
            data[col] = data[col].map(value_translation[col]).fillna(data[col])

    data.columns = [replace_special_characters(col) for col in data.columns]
    
    return data
