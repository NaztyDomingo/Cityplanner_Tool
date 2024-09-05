import pandas as pd



def calculate_heating(data: pd.DataFrame) -> pd.DataFrame:
    oh_data = data[data['Huvudsektor'] == 'Egen uppvärmning av bostäder och lokaler']
    
    oh_data = oh_data[['Län', 'CO2 2022']]
    
    
    heating_summed = data.groupby('Län').sum().reset_index()

    heating_melted = heating_summed.melt(id_vars=['Län'], 
                                         var_name='Year', 
                                         value_name='Other Heating')

    heating_melted['Year'] = heating_melted['Year'].str.replace('CO2 ', '')

    heating_melted = heating_melted.rename(columns={'Län': 'Region'})
    
    return heating_melted





   

