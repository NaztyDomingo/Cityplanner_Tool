import pandas as pd
import os

CURR_DIR_PATH = os.getcwd()
FILE_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/ml_supplementary_data/original/finland'
OUTPUT_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/transformed_supp_data_finland/'

# assign port to region in this dict, use for mapping later
PORT_REG_DICT = {'Pori': 'Satakunta',
                 'Naantali': 'Southwest Finland',
                 'Isnaes': 'Uusimaa',
                 'Merikarvia': 'Satakunta',
                 'Eastern Gulf of Finland': 'Kymenlaakso',
                 'Foegloe': 'Aaland',
                 'Oulu': 'North Ostrobothnia',
                 'Kokkola': 'Central Ostrobothnia',
                 'Haminakotka': 'Kymenlaakso',
                 'Salo': 'Southwest Finland',
                 'Sipoo/Kalkkiranta': 'South Savo',
                 'Varkaus': 'North Savo',
                 'Taalintehdas': 'Southwest Finland',
                 'Kitee': 'North Karelia',
                 'Kemi': 'Lapland',
                 'Vaasa': 'Ostrobothnia',
                 'Eurajoki': 'Satakunta',
                 'Imatra': 'South Karelia',
                 'Laangnaes': 'Aaland',
                 'Koekar': 'Aaland',
                 'Pohjankuru': 'Uusimaa',
                 'Kumlinge': 'Aaland',
                 'Ahkiolahti': 'North Savo',
                 'Godby': 'Aaland',
                 'Hanko': 'Uusimaa',
                 'Skoeldvik': 'Uusimaa',
                 'Kemioe': 'Southwest Finland',
                 'Skogby': 'Uusimaa',
                 'Tolkkinen': 'North Ostrobothnia',
                 'Helsinki': 'Uusimaa',
                 'Savonlinna': 'South Savo',
                 'Iisalmi': 'North Savo',
                 'Kantvik': 'Uusimaa',
                 'Faerjsund': 'Aaland',
                 'Rauma': 'Satakunta',
                 'Houtskaer': 'Southwest Finland',
                 'Foerby': 'Southwest Finland',
                 'Nurmes': 'North Karelia',
                 'Uusikaupunki': 'Southwest Finland',
                 'Juuka': 'North Karelia',
                 'Braendoe': 'Aaland',
                 'Dragsfjaerd': 'Southwest Finland',
                 'Saimaa Others': 'North Savo',
                 'Lappeenranta': 'South Karelia',
                 'Raahe': 'North Ostrobothnia',
                 'Lappohja': 'Uusimaa',
                 'Siilinjaervi': 'North Savo',
                 'Korppoo': 'Southwest Finland',
                 'Rahja': 'North Ostrobothnia',
                 'Inkoo': 'Uusimaa',
                 'Joensuu': 'North Karelia',
                 'Kuopio': 'North Savo',
                 'Maarianhamina': 'Aaland',
                 'Tornio': 'Lapland',
                 'Joutseno': 'South Karelia',
                 'Ristiina': 'South Savo',
                 'Kaskinen': 'Ostrobothnia',
                 'Pietarsaari': 'Ostrobothnia',
                 'Kristiinankaupunki': 'Ostrobothnia',
                 'Parainen': 'Southwest Finland',
                 'Savonranta': 'South Savo',
                 'Turku': 'Southwest Finland',
                 'Loviisa': 'Uusimaa',
                 'Nauvo': 'Southwest Finland',
                 'Eckeroe': 'Aaland'}

AIRPORT_REG_DICT = {'Helsinki-Vantaa': 'Uusimaa',
                    'Enontekioe': 'Lapland',
                    'Ivalo': 'Lapland',
                    'Joensuu': 'North Karelia',
                    'Jyvaeskylae': 'Central Finland',
                    'Kajaani': 'Kainuu',
                    'Kemi-Tornio': 'Lapland',
                    'Kittilae': 'Lapland',
                    'Kokkola-Pietarsaari': 'Ostrobothnia',
                    'Kuopio': 'North Savo',
                    'Kuusamo': 'North Ostrobothnia',
                    'Lappeenranta': 'South Karelia',
                    'Mariehamn': 'Aaland',
                    'Oulu': 'North Ostrobothnia',
                    'Pori': 'Satakunta',
                    'Rovaniemi': 'Lapland',
                    'Savonlinna': 'South Savo',
                    'Tampere-Pirkkala': 'Pirkanmaa',
                    'Turku': 'Southwest Finland',
                    'Vaasa': 'Ostrobothnia'}

ALL_REGIONS = [
    'Aaland', 'Central Finland', 'Central Ostrobothnia', 'Kainuu',
    'Kanta-Haeme', 'Kymenlaakso', 'Lapland', 'North Karelia',
    'North Ostrobothnia', 'North Savo', 'Ostrobothnia', 'Paeijaet-Haeme',
    'Pirkanmaa', 'Satakunta', 'South Karelia', 'South Ostrobothnia',
    'South Savo', 'Southwest Finland', 'Uusimaa'
]

REGION_TRANSLATION_DICT = {
    'Varsinais-Suomi': 'Southwest Finland',
    'Etelae-Savo': 'South Savo',
    'Pohjois-Savo': 'North Savo',
    'South-Savo': 'South Savo',
}


def main() -> None:
    run_once_to_transform()
    print('All files transformed...')


def run_once_to_transform():
    ship_car_df = transform_ship_and_car_data()
    airplane_df = transform_airplane_data()
    consumption_population_df = transform_energy_and_population_data()
    agriculture_df = transform_agricultural_data()

    energy_agric_df = pd.merge(consumption_population_df, agriculture_df, on=[
                        'Year', 'Region'], how='inner')
    energy_agric_df = energy_agric_df.rename(columns={'Energy Use In Tj': 'Industry Energy Use In Tj', 'Oil Gas Floor Area m2': 'Oil Gas Floor Heating of Floor Area m2', 'Coal Coke Floor Area m2': 'Coal Coke Heating of Floor Area m2',
                                        'Wood Peat Floor Area m2': 'Wood Peat Heating of Floor Area m2', 'Other Floor Area m2': 'Other Heating of Floor Area m2', 'Utilized Agric Area': 'Utilized Agric Area in m2'})
    energy_agric_df.to_csv(OUTPUT_PATH + 'energy_agric_fin.csv', index=False)

    final_df = pd.merge(energy_agric_df, ship_car_df, on=['Year', 'Region'], how='inner')

    final_df.to_csv(OUTPUT_PATH + 'supplementary_data_fin.csv', index=False)

def create_df(file: str) -> pd.DataFrame:
    df = pd.read_csv(f'{FILE_PATH}/{file}.csv')
    return df


def remove_prefix(df: pd.DataFrame, old_column: str, new_column: str, prefix_length: str) -> pd.DataFrame:
    df[new_column] = df[old_column].str[prefix_length:]
    return df


def translate_regions(df: pd.DataFrame, replacements: dict) -> pd.DataFrame:
    return df.replace(replacements)

# converts year to type int and drops column(s)


def clean_df(df: pd.DataFrame, columns_to_drop: list, int_columns: list = [], year_col: str = 'Year') -> pd.DataFrame:
    df = df.drop(columns=columns_to_drop, errors='ignore')
    if year_col in df:
        df[year_col] = df[year_col].astype(int)
        # Convert specified columns to integers
    for col in int_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)
    return df


def remove_mk(df, col_name) -> pd.DataFrame:
    df = remove_prefix(df, col_name, 'Region', 5)
    # errors='ignore' only drops area if exists
    df = df.drop('Area', axis=1, errors='ignore')
    return df

# func to add region to rows based on port/airport


def assign_region(df, column: str, dict):
    df['Region'] = df[column].map(dict)
    df = df.drop(column, axis=1)  # rm column after region is assigned
    return df


## agriculture ##


def transform_agricultural_data():

    agric_area_df = create_df('agric_area_fin')
    agric_area_df = agric_area_df.drop('Variable', axis=1)
    agric_area_df = clean_df(agric_area_df, ['Variable'])

    # rm 2010 from df for consistency before merge
    # agric_area_df = agric_area_df[agric_area_df['Year'] != 2010]

    livestock_df = create_df('livestock_num_fin')
    livestock_df = livestock_df.drop('Variable', axis=1)
    livestock_df = clean_df(livestock_df, ['Variable'])

    agriculture_df = pd.merge(agric_area_df, livestock_df, on=[
        'Year', 'Region'], how='inner')

    agriculture_df = translate_regions(agriculture_df, REGION_TRANSLATION_DICT)
    agriculture_df = agriculture_df.replace('..', 0)

    agriculture_df.to_csv(f"{OUTPUT_PATH}agriculture_fin.csv", index=False)

    return agriculture_df

## transportation ##


def transform_ship_and_car_data() -> pd.DataFrame:

    cars_df = create_df('reg_cars_fin')
    cars_df = remove_mk(cars_df, 'Area')

    # melt df to get correct format for merging later
    melted_df = pd.melt(
        cars_df, id_vars=['Region'], var_name='Year', value_name='Num of Vehicles')
    melted_df['Year'] = melted_df['Year'].str[16:].astype(int)
    cars_df = melted_df.sort_values(
        by=['Year', 'Region']).reset_index(drop=True)


    ship_int_df = create_df('ship_international_fin')
    ship_passenger_df = create_df('ship_passenger_traffic_fin')

    ship_int_df = ship_int_df.replace('.', 0)
    ship_passenger_df = ship_passenger_df.replace('.', 0)

    ship_int_df = clean_df(ship_int_df, [], ['Tons of Ship Cargo'])
    ship_passenger_df = clean_df(ship_passenger_df, [], ['Num of Ship Passengers'])

    # added explicit conversion here due to trouble with clean_df func (will fix properly later)
    ship_int_df['Tons Of Ship Cargo'] = pd.to_numeric(ship_int_df['Tons Of Ship Cargo'], errors='coerce').fillna(0).astype(int)
    ship_passenger_df['Num Of Ship Passengers'] = pd.to_numeric(ship_passenger_df['Num Of Ship Passengers'], errors='coerce').fillna(0).astype(int)

    # assign regions based on ports
    ship_int_df = assign_region(ship_int_df, 'Port', PORT_REG_DICT)
    ship_passenger_df = assign_region(ship_passenger_df, 'Port', PORT_REG_DICT)

    ship_int_df = ship_int_df.groupby(['Year', 'Region']).sum().reset_index()
    ship_passenger_df = ship_passenger_df.groupby(['Year', 'Region']).sum().reset_index()

    ships_df = pd.merge(ship_int_df, ship_passenger_df, on=[
                        'Year', 'Region'], how='inner')
    

    shipping_cars_df = pd.merge(ships_df, cars_df, on=[
                                'Year', 'Region'], how='right')
    shipping_cars_df = shipping_cars_df.rename(
        columns={"Num of Vehicles": "Num of Registered Automobiles"})

    shipping_cars_df.fillna(0, inplace=True)

    shipping_cars_df.to_csv(
        OUTPUT_PATH + 'transportation_fin.csv', index=False)

    return shipping_cars_df


def transform_airplane_data() -> pd.DataFrame:
    airplane_df = create_df('airplane_fin')
    airplane_df = clean_df(airplane_df, [])
    airplane_df = assign_region(airplane_df, 'Airport', AIRPORT_REG_DICT)

    airplane_df.to_csv(
        f'{OUTPUT_PATH}air_passenger_and_cargo_transport_fin.csv', index=False)

    return airplane_df


## Energy ##

def transform_energy_and_population_data():
    COLUMNS_TO_DROP = ['Long Distance Or Reg Heating Gross Floor Area (m2)',
                       'Electricity Floor Area m2', 'Ground Heat Floor Area m2']

    heating_df = create_df('heating_buildings_by_m2_fin')
    heating_df = remove_mk(heating_df, 'Area')
    heating_df = clean_df(heating_df, COLUMNS_TO_DROP)

    industry_energy_df = create_df('ind_energy_consum_fin')
    industry_energy_df = remove_mk(industry_energy_df, 'Region')
    industry_energy_df = clean_df(industry_energy_df, [])
    industry_energy_df = translate_regions(
       industry_energy_df, REGION_TRANSLATION_DICT)

    energy_df = pd.merge(industry_energy_df, heating_df,
                          on=['Year', 'Region'], how='inner')

    wood_consumption_df = create_df('wood_consum_fin')
    wood_consumption_df = clean_df(wood_consumption_df, ['Unit'])

    wood_consumption_df['Region'] = wood_consumption_df['Region'].str.replace(
        r'^\d+\s+', '', regex=True)  # use regex to rm the numerical region prefixes

    wood_consumption_df = translate_regions(
        wood_consumption_df, REGION_TRANSLATION_DICT)

    energy_fuel_consumption_df = pd.merge(heating_df, wood_consumption_df, on=[
        'Year', 'Region'], how='inner')

    population_df = create_df('population_fin')
    population_df = clean_df(population_df, ['Information'])

    melted_pop_df = pd.melt(population_df, id_vars=[
                            'Year'], var_name='Region', value_name='population')
    melted_pop_df = remove_mk(melted_pop_df, 'Region')

    consumption_population_df = pd.merge(
        energy_fuel_consumption_df, melted_pop_df, on=['Year', 'Region'], how='inner')

    consumption_population_df.to_csv(
        f'{OUTPUT_PATH}energy_consumption_and_population_fin.csv', index=False)

    return consumption_population_df


# execute transformations
if __name__ == "__main__":
    main()
