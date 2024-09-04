import read_data as rd
import translate_replace as tr
import pandas as pd
import os
import glob

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

file_path = glob.glob(os.path.join(CURR_DIR_PATH, 'countyreport_emissions.csv'))[0]

output_file = os.path.join(CURR_DIR_PATH, 'emissions_by_municipality.csv')

def filter_and_save_data(data: pd.DataFrame, output_file: str) -> None:
    
    print(f'Data after translate_replace: {data}')

    filtered_data = data[(data['Main sector'] == 'Alla') & (data['Subsector'] == 'Alla')]
    
    print(filtered_data)

    filtered_data = filtered_data.drop(columns=['Main sector', 'Subsector', 'Total greenhouse gases in CO2-equivalent 2000'])
    
    print(filtered_data)

    municipalities_to_keep = [
        ('Blekinge county', 'Karlskrona'),
        ('Dalarnas county', 'Borlaenge'),
        ('Gotlands county', 'Gotland'),
        ('Gaevleborgs county', 'Gaevle'),
        ('Hallands county', 'Halmstad'),
        ('Jaemtlands county', 'OEstersund'),
        ('Joenkoepings county', 'Joenkoeping'),
        ('Kalmar county', 'Kalmar'),
        ('Kronobergs county', 'Vaexjoe'),
        ('Norrbottens county', 'Gaellivare'),
        ('Skaane county', 'Malmoe'),
        ('Stockholms county', 'Stockholm'),
        ('Soedermanlands county', 'Nykoeping'),
        ('Uppsala county', 'Uppsala'),
        ('Vaermlands county', 'Karlstad'),
        ('Vaesterbottens county', 'Skellefteaa'),
        ('Vaesternorrlands county', 'OErnskoeldsvik'),
        ('Vaestmanlands county', 'Vaesteraas'),
        ('Vaestra Goetalands county', 'Goeteborg'),
        ('OErebro county', 'OErebro'),
        ('OEstergoetlands county', 'Linkoeping')
    ]
    
    filtered_data = filtered_data[
        filtered_data[['County', 'Municipality']].apply(tuple, axis=1).isin(municipalities_to_keep)
    ]
    
    print(filtered_data)

    filtered_data.to_csv(output_file, index=False)
    


data = rd.read_file(file_path)
        
data = tr.rename_columns(data)

data = tr.drop_second_row(data)

filter_and_save_data(data, output_file)
    
   

