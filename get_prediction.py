from statsmodels.tsa.vector_ar.var_model import VAR
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import filehandler_helper as fh
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

def main() -> None:
    #output_predictions('sweden_regions_emissions.csv', 'sweden', 'region') # get some problems due to null values and 'total emissions' = object
    #output_predictions('finland_regions_emissions.csv', 'finland', 'region')
    #output_predictions('finland_cities_emissions.csv', 'finland', 'city' )
    #output_predictions('sweden_cities_emissions.csv', 'sweden', 'city' )

    plot_predictions('finland_cities_emissions.csv', 'finland', 'city' )
   
    print('All predictions converted to csv...')

def prep_dfs(input_file: str, country: str, type: str) -> list:
    
    region_or_city = type.capitalize()

    filename = input_file
    folder = f'transformed_{country}_data'
    filepath = fh.get_path_of_file(folder, filename)

    emission_df = pd.read_csv(filepath)
    emission_df['Year'] = pd.to_datetime(emission_df['Year'], format='%Y')

    if region_or_city == 'City':
        emission_df = emission_df.drop('Region', axis=1)
        emission_df = emission_df.drop_duplicates()
    elif country == 'sweden':
        emission_df['Total Emissions'] = emission_df['Total Emissions'].astype(float)
        print(emission_df.dtypes)
    
    emission_df_2010 = emission_df[emission_df['Year'] >= '2010-01-01']

    emission_pivot = emission_df.pivot(index='Year', columns=region_or_city, values='Total Emissions') #used in concat later
    emission_pivot_2010 = emission_df_2010.pivot(index='Year', columns=region_or_city, values='Total Emissions') #used in predictions

    df_list = [emission_pivot, emission_pivot_2010]

    return df_list

def get_predictions(input_file: str, country: str, type: str) -> pd.Series:
    
    dfs = prep_dfs(input_file, country, type)
    emission_pivot = dfs[0]
    emission_pivot_2010 = dfs[1]

    emission_pivot_log = np.log(emission_pivot_2010) # np.log to reduce range of data and stabilize variance

    # do .diff() to make data stationary (e.g. mean doesnt't change along time series). 
    emission_pivot_diff = emission_pivot_log.diff().dropna() # calcs difference between each element and the previous, need dropna because a NaN is introduced as first entry has no prev entry

    model = VAR(emission_pivot_diff)
    model_fit = model.fit()

    forecast_steps = 3 # steps = number of years to forecast
    lag_order = model_fit.k_ar # retrieve optimal lag_order (= amount of previous steps used in model) from model_fit

    forecast_input = emission_pivot_diff.values[-lag_order:] # conv to np array, slice last lag_order to use when forecasting. If lag_order = 3, returns array with 3 nested arrays with 19 entries(each region)
    forecast_diff = model_fit.forecast(y=forecast_input, steps=forecast_steps) # returns array with nested array of forecasted data for each step, predictions also in diffferences 

    # create range of future years, length matching steps
    forecast_index = pd.date_range(
        # start at last known data point, starts forecast at start + 1 year and predicts three years
        start=emission_pivot_2010.index[-1] + pd.DateOffset(years=1), periods=forecast_steps, freq='YS') # YS = year start, start of year as frequency (yyyy-01-01)

    # create a forecast df (three rows, matching steps): use prev range as index, forecast_diff as values and get column names from emission_pivot (need to be identical for later)
    forecast_diff_df = pd.DataFrame(
        forecast_diff, index=forecast_index, columns=emission_pivot_2010.columns)

    # conv forecast back to original scale 
    last_log_values = emission_pivot_log.iloc[-1]
    forecast_log_original = last_log_values + forecast_diff_df.cumsum() # cumulative sum of forecast diff values, basically undo the diff
    forecast_original = np.exp(forecast_log_original) # "undo" the log operation

    # append forecast data (now in original scale) to historical data
    combined_series = pd.concat([emission_pivot, forecast_original])

    return combined_series

def output_predictions(input_file: str, country: str, type: str) -> None:

    output_file = f'{country}_{type}_predictions.csv'
    output_folder = 'transformed_predictions'
    output_path = fh.get_path_of_file(output_folder, output_file)
    
    combined_series = get_predictions(input_file, country, type)
    combined_series.index.name = 'Year'
    combined_series.index = combined_series.index.year
    combined_series.to_csv(output_path)

def plot_predictions(input_file: str, country: str, type: str):
    combined_series = get_predictions(input_file, country, type)

    #conv back to dt for plotting purposes
    #combined_series.index = pd.to_datetime(combined_series.index, format='%Y')

    combined_series.plot(figsize=(10, 6), marker='o')
    plt.axvline(x=combined_series.index[-4], color='red',
                linestyle='--', label='2022 (Last Known Data Point)') #vertical line to mark split between historical/forecast data
    plt.xlabel('Year')
    plt.ylabel('Emissions')
    plt.title(f'{type.capitalize()}-wide Emissions Forecast (2023-2025) for {country.capitalize()}')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

