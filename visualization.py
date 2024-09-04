import filehandler_helper as fh
import os
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd

# Load and prepare data
def load_data():
    
    # Read csv files to get data
    # Finland data
    filepath = fh.get_path_of_folder('transformed_finland_data')
    filepath_of_fin_cities = os.path.join(filepath, 'finland_cities_emissions.csv')
    filepath_of_fin_regions = os.path.join(filepath, 'finland_regions_emissions.csv')
    fin_cities_df = pd.read_csv(filepath_of_fin_cities)
    fin_regions_df = pd.read_csv(filepath_of_fin_regions)

    # Sweden data
    # TBA

    # Combine SWE+FIN city data
    # Combine SWE+FIN region data ?

    # Tree data
    filepath = fh.get_path_of_folder('transformed_tree_data')
    filepath_of_trees = os.path.join(filepath, 'final_tree_info.csv')
    tree_df = pd.read_csv(filepath_of_trees)

    # Dash example:
    df = pd.DataFrame({
        'Category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'],
        'Variable': ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z'],
        'Values': [4, 3, 6, 1, 5, 7, 2, 8, 5, 5, 7, 6]
    })

    list_of_dfs = [fin_cities_df, fin_regions_df, tree_df, df]
    return list_of_dfs

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Dash Data Visualization"

# Load and unpack dfs
dfs = load_data()
fin_cities_df, fin_regions_df, tree_df, df = dfs

# Define the layout of the app
app.layout = html.Div([
    html.H1("Data Visualization Dashboard", style={'textAlign': 'center'}),
    
    # Input field for the user to type in a variable name
    dcc.Input(
        id='variable-input',
        type='text',
        placeholder='Enter a city',
        style={'width': '300px'}
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    
    # Graph component to display the plot
    dcc.Graph(id='line-chart'),

    # Some additional controls or elements
    html.Div(id='output-container', style={'margin-top': 20})
])

# Define the callback for the input field and button
@app.callback(
    Output('line-chart', 'figure'),
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('variable-input', 'value')
)

def update_graph(n_clicks, input_value):
    if n_clicks > 0 and input_value:
        # Filter data based on user input
        fin_city_df = fin_cities_df[fin_cities_df['Hinku calculation without emission credits'] == 'total emissions, ktCO2e']
        filtered_data = fin_city_df[fin_city_df['City'].str.contains(input_value, case=False)]
        
        if not filtered_data.empty:
            # Convert the DataFrame from wide to long format for plotting
            # years = ['1990'] + [str(year) for year in range(2005, 2023)] # if you wanna add 1990, messed up x-scale though
            melted_data = filtered_data.melt(id_vars=['City'], value_vars=[str(year) for year in range(2005, 2023)],
                                             var_name='Year', value_name='Total Emissions (ktCO2e)')

            # Ensure the 'Year' column is numeric for plotting
            melted_data['Year'] = pd.to_numeric(melted_data['Year'])

            # Create a line chart
            fig = px.line(
                melted_data,
                x='Year',
                y='Total Emissions (ktCO2e)',
                title=f'Total Emissions for {input_value.capitalize()}'
            )
            fig.update_xaxes(
                tickmode='array',  # Define ticks manually
                tickvals=list(range(2005, 2023)),
                # tickangle=75
            )

            return fig, f'Showing data for city: {input_value.capitalize()}'
        else:
            return {}, 'No data available for the input city.'

    # Initial display or when input is invalid
    return {}, 'Please enter a valid city.'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

