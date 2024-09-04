import pandas as pd
import os

CURR_DIR_PATH = os.getcwd()
FILE_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/ml_supplementary_data/original/finland'
OUTPUT_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/ml_supplementary_data/output/'

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
    "Aaland", "Central Finland", "Central Ostrobothnia", "Kainuu", 
    "Kanta-Haeme", "Kymenlaakso", "Lapland", "North Karelia", 
    "North Ostrobothnia", "North Savo", "Ostrobothnia", "Paeijaet-Haeme", 
    "Pirkanmaa", "Satakunta", "South Karelia", "South Ostrobothnia", 
    "South Savo", "Southwest Finland", "Uusimaa"
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

    final_df = pd.merge(consumption_population_df, agriculture_df, on=[
                        'year', 'region'], how='inner')
    final_df = final_df.rename(columns={'energy_use_in_tj': 'industry_energy_use_in_tj', 'oil_gas_floor_area_m2': 'oil_gas_heating_of_floor_area_in_m2', 'coal_coke_floor_area_m2': 'coal_coke_heating_of_floor_area_in_m2',
                                        'wood_peat_floor_area_m2': 'wood_peat_heating_of_floor_area_in_m2', 'other_floor_area_m2': 'other_heating_of_floor_area_in_m2', 'utilized_agric_area': 'utilized_agric_area_in_1000_hectares'})
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


def clean_df(df: pd.DataFrame, columns_to_drop: list, year_col: str = 'year') -> pd.DataFrame:
    df = df.drop(columns=columns_to_drop, errors='ignore')
    if year_col in df:
        df[year_col] = df[year_col].astype(int)
    return df


def remove_mk(df, col_name) -> pd.DataFrame:
    df = remove_prefix(df, col_name, 'region', 5)
    # errors='ignore' only drops area if exists
    df = df.drop('area', axis=1, errors='ignore')
    return df

# func to add region to rows based on port/airport


def assign_region(df, column: str, dict):
    df['region'] = df[column].map(dict)
    df = df.drop(column, axis=1)  # rm column after region is assigned
    return df


## agriculture ##


def transform_agricultural_data():

    agric_area_df = create_df('agric_area_fin')
    agric_area_df = agric_area_df.drop('variable', axis=1)
    agric_area_df = clean_df(agric_area_df, ['variable'])

    # rm 2010 from df for consistency before merge
    # agric_area_df = agric_area_df[agric_area_df['year'] != 2010]

    livestock_df = create_df('livestock_num_fin')
    livestock_df = livestock_df.drop('variable', axis=1)
    livestock_df = clean_df(livestock_df, ['variable'])

    agriculture_df = pd.merge(agric_area_df, livestock_df, on=[
        'year', 'region'], how='inner')

    agriculture_df = translate_regions(agriculture_df, REGION_TRANSLATION_DICT)
    agriculture_df = agriculture_df.replace('..', 0)

    agriculture_df.to_csv(f"{OUTPUT_PATH}agriculture_fin.csv", index=False)

    return agriculture_df

## transportation ##


def transform_ship_and_car_data() -> pd.DataFrame:
    # Read and clean dataframes
    cars_df = create_df('reg_cars_fin')
    cars_df = remove_mk(cars_df, 'area')

    # Melt df to get correct format for merging later
    melted_df = pd.melt(cars_df, id_vars=['region'], var_name='year', value_name='num_of_vehicles')
    melted_df['year'] = melted_df['year'].str[16:].astype(int)
    cars_df = melted_df.sort_values(by=['year', 'region']).reset_index(drop=True)

    # Remove data before 2016
    cars_df = cars_df[cars_df.year >= 2016]

    # Load and clean ship data
    ship_int_df = create_df('ship_international_fin')
    ship_passenger_df = create_df('ship_passenger_traffic_fin')
    ship_traffic_df = create_df('ship_traffic_fin')
    
    # Clean dataframes
    ship_int_df = clean_df(ship_int_df, [])
    ship_passenger_df = clean_df(ship_passenger_df, [])
    ship_traffic_df = clean_df(ship_traffic_df, [])

    # Assign regions
    ship_int_df = assign_region(ship_int_df, 'port', PORT_REG_DICT)
    ship_passenger_df = assign_region(ship_passenger_df, 'port', PORT_REG_DICT)
    ship_traffic_df = assign_region(ship_traffic_df, 'port', PORT_REG_DICT)

    # Merge ship dataframes
    ships_df = pd.merge(ship_traffic_df, ship_int_df, on=['year', 'region'], how='inner')
    ships_df = pd.merge(ships_df, ship_passenger_df, on=['year', 'region'], how='outer')

    # Convert numeric columns to appropriate types
    ships_df['num_of_ship_visits'] = pd.to_numeric(ships_df['num_of_ship_visits'], errors='coerce')
    ships_df['tons_of_ship_cargo'] = pd.to_numeric(ships_df['tons_of_ship_cargo'], errors='coerce')
    ships_df['num_of_ship_passengers'] = pd.to_numeric(ships_df['num_of_ship_passengers'], errors='coerce')

    # Aggregate to get one row per year*region
    aggregated_shipping_df = ships_df.groupby(['year', 'region']).agg({
        'num_of_ship_visits': 'sum',
        'tons_of_ship_cargo': 'sum',
        'num_of_ship_passengers': 'sum'
    }).reset_index()

    # Merge with car data
    shipping_cars_df = pd.merge(aggregated_shipping_df, cars_df, on=['year', 'region'], how='right')
    shipping_cars_df = shipping_cars_df.rename(columns={"num_of_vehicles": "num_of_registered_automobiles"})

    shipping_cars_df.fillna(0, inplace=True)

    # Save the final dataframe
    shipping_cars_df.to_csv(OUTPUT_PATH + 'transportation_fin.csv', index=False)

    print(shipping_cars_df.dtypes)

    return shipping_cars_df


def transform_airplane_data() -> pd.DataFrame:
    airplane_df = create_df('airplane_fin')
    airplane_df = clean_df(airplane_df, [])
    airplane_df = assign_region(airplane_df, 'airport', AIRPORT_REG_DICT)

    airplane_df.to_csv(
        f'{OUTPUT_PATH}air_passenger_and_cargo_transport_fin.csv', index=False)

    return airplane_df


## Energy ##

def transform_energy_and_population_data():
    COLUMNS_TO_DROP = ['long_distance_or_reg_heating_gross_floor_area_(m2)',
                       'electricity_floor_area_m2', 'ground_heat_floor_area_m2']

    heating_df = create_df('heating_buildings_by_m2_fin')
    heating_df = remove_mk(heating_df, 'area')
    heating_df = clean_df(heating_df, COLUMNS_TO_DROP)

    industry_energy_df = create_df('ind_energy_consum_fin')
    industry_energy_df = remove_mk(industry_energy_df, 'region')
    industry_energy_df = clean_df(industry_energy_df, [])
    industry_energy_df = translate_regions(
        industry_energy_df, REGION_TRANSLATION_DICT)

    energy_df = pd.merge(industry_energy_df, heating_df,
                         on=['year', 'region'], how='inner')

    wood_consumption_df = create_df('wood_consum_fin')
    wood_consumption_df = clean_df(wood_consumption_df, ['unit'])

    wood_consumption_df['region'] = wood_consumption_df['region'].str.replace(
        r'^\d+\s+', '', regex=True)  # use regex to rm the numerical region prefixes

    wood_consumption_df = translate_regions(
        wood_consumption_df, REGION_TRANSLATION_DICT)

    energy_fuel_consumption_df = pd.merge(energy_df, wood_consumption_df, on=[
        'year', 'region'], how='inner')

    population_df = create_df('population_fin')
    population_df = clean_df(population_df, ['Information'])

    melted_pop_df = pd.melt(population_df, id_vars=[
                            'year'], var_name='region', value_name='population')
    melted_pop_df = remove_mk(melted_pop_df, 'region')

    consumption_population_df = pd.merge(
        energy_fuel_consumption_df, melted_pop_df, on=['year', 'region'], how='inner')

    consumption_population_df.to_csv(
        f'{OUTPUT_PATH}energy_consumption_and_population_fin.csv', index=False)

    return consumption_population_df


# execute transformations
if __name__ == "__main__":
    main()
