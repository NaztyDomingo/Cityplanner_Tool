import pandas as pd
import os

CURR_DIR_PATH = os.getcwd()
FILE_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/ml_supplementary_data/original/finland'
OUTPUT_PATH = CURR_DIR_PATH + \
    '/Cityplanner_Tool/data/ml_supplementary_data/output/'


def create_df(file: str):
    df = pd.read_csv(FILE_PATH + '/' + file + '.csv')
    return df


def remove_prefix(df, old_column: str, new_column: str, prefix_length: str):
    df[new_column] = df[old_column].str[prefix_length:]
    return df


def remove_mk(df, col_name):
    df = remove_prefix(df, col_name, 'region', 5)
    # errors='ignore' only drops area if exists
    df = df.drop('area', axis=1, errors='ignore')
    return df


def conv_year(df):
    df['year'] = df['year'].astype(int)
    return df

# func to add region to rows based on port/airport


def assign_region(df, column: str, dict):
    df['region'] = df[column].map(dict)
    return df


# assign port to region in this dict, use for mapping later
port_reg_dict = {'Pori': 'Satakunta',
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

airport_reg_dict = {'Helsinki-Vantaa': 'Uusimaa',
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

## agriculture ##


def transform_agricultural_data():

    agric_area_df = create_df('agric_area_fin')
    agric_area_df = agric_area_df.drop('variable', axis=1)
    agric_area_df = conv_year(agric_area_df)

    # rm 2010 from df for consistency before merge
    agric_area_df = agric_area_df[agric_area_df['year'] != 2010]

    livestock_df = create_df('livestock_num_fin')
    livestock_df = livestock_df.drop('variable', axis=1)
    livestock_df = conv_year(livestock_df)

    agriculture_df = pd.merge(agric_area_df, livestock_df, on=[
        'year', 'region'], how='inner')
    agriculture_df = agriculture_df.replace(
        'Varsinais-Suomi', 'Southwest Finland')
    agriculture_df = agriculture_df.replace('Etelae-Savo', 'South Savo')
    agriculture_df = agriculture_df.replace('Pohjois-Savo', 'North Savo')
    agriculture_df = agriculture_df.replace('..', 0)

    agriculture_df.to_csv(OUTPUT_PATH + 'agriculture_fin.csv', index=False)

    return agriculture_df

## transportation ##


def transform_ship_and_car_data():

    cars_df = create_df('reg_cars_fin')
    cars_df = remove_mk(cars_df, 'area')

    # melt df to get correct format for merging later
    melted_df = pd.melt(
        cars_df, id_vars=['region'], var_name='year', value_name='num_of_vehicles')

    melted_df['year'] = melted_df['year'].str[16:].astype(
        int)  # rm 'num_of_vehicles_' prefix from year column
    cars_df = melted_df.sort_values(
        by=['year', 'region']).reset_index(drop=True)

    cars_df = cars_df.drop(cars_df[cars_df.year < 2016].index)

    # define df's and extract each unq port
    ship_int_df = create_df('ship_international_fin')
    ship_int_df = conv_year(ship_int_df)

    ship_passenger_df = create_df('ship_passenger_traffic_fin')
    ship_passenger_df = conv_year(ship_passenger_df)

    ship_traffic_df = create_df('ship_traffic_fin')
    ship_traffic_df = conv_year(ship_traffic_df)

    ship_int_df = assign_region(ship_int_df, 'port', port_reg_dict)
    ship_passenger_df = assign_region(ship_passenger_df, 'port', port_reg_dict)
    ship_traffic_df = assign_region(ship_traffic_df, 'port', port_reg_dict)

    # rm port now that region is in place
    ship_int_df = ship_int_df.drop('port', axis=1)
    ship_passenger_df = ship_passenger_df.drop('port', axis=1)
    ship_traffic_df = ship_traffic_df.drop('port', axis=1)

    # merge df's
    ships_df = pd.merge(ship_traffic_df, ship_int_df, on=[
                        'year', 'region'], how='outer')
    ships_df = pd.merge(ships_df, ship_passenger_df, on=[
                        'year', 'region'], how='outer')

    # change datatypes from str to int for numeric cols
    ships_df['num_of_ship_visits'] = pd.to_numeric(
        ships_df['num_of_ship_visits'], errors='coerce')
    ships_df['tons_of_ship_cargo'] = pd.to_numeric(
        ships_df['tons_of_ship_cargo'], errors='coerce')
    ships_df['num_of_ship_passengers'] = pd.to_numeric(
        ships_df['num_of_ship_passengers'], errors='coerce')

    # aggregate to get only one row per year*region
    aggregated_shipping_df = ships_df.groupby(['year', 'region']).agg({
        'num_of_ship_visits': 'sum',
        'tons_of_ship_cargo': 'sum',
        'num_of_ship_passengers': 'sum'
    }).reset_index()

    ship_cars_df = pd.merge(aggregated_shipping_df, cars_df, on=[
                            'year', 'region'], how='inner')

    ship_cars_df.to_csv(OUTPUT_PATH + 'transportation_fin.csv', index=False)

    return ship_cars_df


def transform_airplane_data():
    airplane_df = create_df('airplane_fin')
    airplane_df = conv_year(airplane_df)
    airplane_df = assign_region(airplane_df, 'airport', airport_reg_dict)

    airplane_df.to_csv(
        OUTPUT_PATH + 'air_passenger_and_cargo_transport_fin.csv', index=False)

    return airplane_df


## Energy ##

def transform_energy_and_population_data():

    heating_df = create_df('heating_buildings_by_m2_fin')
    heating_df = remove_mk(heating_df, 'area')
    heating_df = heating_df.drop(['long_distance_or_reg_heating_gross_floor_area_(m2)',
                                  'electricity_floor_area_m2', 'ground_heat_floor_area_m2'], axis=1)
    heating_df = conv_year(heating_df)

    industry_energy_consum_df = create_df('ind_energy_consum_fin')
    industry_energy_consum_df = remove_mk(industry_energy_consum_df, 'region')
    industry_energy_consum_df = conv_year(industry_energy_consum_df)
    industry_energy_consum_df = industry_energy_consum_df.drop(
        industry_energy_consum_df[industry_energy_consum_df.year < 2010].index)

    industry_energy_consum_df = industry_energy_consum_df.replace(
        'Varsinais-Suomi', 'Southwest Finland')
    industry_energy_consum_df = industry_energy_consum_df.replace(
        'South-Savo', 'South Savo')
    industry_energy_consum_df = industry_energy_consum_df.replace(
        'Pohjois-Savo', 'North Savo')

    energy_df = pd.merge(industry_energy_consum_df, heating_df,
                         on=['year', 'region'], how='inner')

    wood_consumption_df = create_df('wood_consum_fin')
    wood_consumption_df = wood_consumption_df.drop('unit', axis=1)
    wood_consumption_df = conv_year(wood_consumption_df)

    wood_consumption_df['region'] = wood_consumption_df['region'].str.replace(
        r'^\d+\s+', '', regex=True)  # use regex to rm the numerical region prefixes

    wood_consumption_df = wood_consumption_df.replace(
        'Varsinais-Suomi', 'Southwest Finland')
    wood_consumption_df = wood_consumption_df.replace(
        'Etelae-Savo', 'South Savo')
    wood_consumption_df = wood_consumption_df.replace(
        'Pohjois-Savo', 'North Savo')

    energy_fuel_consumption_df = pd.merge(energy_df, wood_consumption_df, on=[
        'year', 'region'], how='inner')

    population_df = create_df('population_fin')
    population_df = population_df.drop('Information', axis=1)

    melted_pop_df = pd.melt(population_df, id_vars=[
                            'year'], var_name='region', value_name='population')
    melted_pop_df = remove_mk(melted_pop_df, 'region')

    consumption_population_df = pd.merge(
        energy_fuel_consumption_df, melted_pop_df, on=['year', 'region'], how='inner')

    consumption_population_df.to_csv(
        OUTPUT_PATH + 'energy_consumption_and_population_fin.csv', index=False)

    return consumption_population_df


ship_car_df = transform_ship_and_car_data()
airplane_df = transform_airplane_data()
consumption_population_df = transform_energy_and_population_data()
agriculture_df = transform_agricultural_data()

final_df = pd.merge(consumption_population_df, agriculture_df, on=[
                    'year', 'region'], how='inner')
final_df = final_df.rename(columns={'energy_use_in_tj': 'industry_energy_use_in_tj', 'oil_gas_floor_area_m2': 'oil_gas_heating_of_floor_area_in_m2', 'coal_coke_floor_area_m2': 'coal_coke_heating_of_floor_area_in_m2',
                           'wood_peat_floor_area_m2': 'wood_peat_heating_of_floor_area_in_m2', 'other_floor_area_m2': 'other_heating_of_floor_area_in_m2', 'utilized_agric_area': 'utilized_agric_area_in_1000_hectares'})
final_df.to_csv(OUTPUT_PATH + 'supplementary_data_fin.csv', index=False)
