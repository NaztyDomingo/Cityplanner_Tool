import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima

CURR_DIR_PATH = os.getcwd()
FILE_PATH = CURR_DIR_PATH + '/Cityplanner_Tool/data/'

# def region
region = 'Aaland'

emission_df = pd.read_csv(f'{FILE_PATH}transformed_finland_data/finland_regions_emissions.csv')

# use reg to filter df
emission_df = emission_df[emission_df['Region'] == region].copy()
emission_df['Year'] = pd.to_datetime(emission_df['Year'], format='%Y')

X = emission_df['Year'].to_list()
y = emission_df['Total Emissions'].to_list()

# log transformation to stabilize
emission_series = pd.Series(np.log(y), index=X)

# check arima metrics
emission_series_diff = emission_series.diff().dropna()
result = adfuller(emission_series_diff)
print('ADF Statistic after log transformation:', result[0])
print('p-value after log transformation:', result[1])

# auto model to find best (p,d,q)
auto_model = auto_arima(emission_series, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
print(f"Optimal ARIMA model: {auto_model.order}")

# fit model
model = ARIMA(emission_series_diff, order=(0, 1, 2))
model_fit = model.fit()

# forecats three years (steps) ahead
forecast_log_diff = model_fit.forecast(steps=3)

last_year = emission_series.index[-1]

# conv back from log to original scale 
forecast_years = [last_year + pd.DateOffset(years=i) for i in range(1, 4)]
forecast_log_original = emission_series.iloc[-1] + forecast_log_diff.cumsum()
forecast_original = np.exp(forecast_log_original)  # Apply exponential to reverse log transformation
forecast_original.index = forecast_years

# combine actual and forecasted data
combined_series = pd.Series(np.exp(emission_series), index=X)  # Convert back to original scale
combined_series = combined_series._append(forecast_original)
print(combined_series)

plt.figure(figsize=(10, 6))
plt.plot(combined_series.index, combined_series, label='Historical and Forecasted Emissions', marker='o')
plt.axvline(x=emission_series.index[-1], color='red', linestyle='--', label='2022 (Last Known Data Point)')
plt.xlabel('Year')
plt.ylabel('Emissions')
plt.title('Emissions Forecast (2023-2025)')
plt.legend()
plt.show()

