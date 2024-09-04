import filehandler_helper as fh
import os
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd
import visualization_data as vd

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Dash Data Visualization"

# Load and unpack dfs
dfs = vd.load_data()
fin_cities_df, fin_regions_df, tree_df, df = dfs

# Define the layout of the app
app.layout = html.Div([
    html.H1("Cityplanner Tool", style={'textAlign': 'center'}),
    
    # Input field for the user to type in a variable name
    dcc.Input(
        id='variable-input',
        type='text',
        placeholder='Enter a city',
        style={'width': '300px'}
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    
    # Container for the two graphs side by side
    html.Div([
        # Line chart for emissions over years
        dcc.Graph(id='line-chart', style={'display': 'inline-block', 'width': '62%'}),
        
        # Pie chart for emissions by source
        dcc.Graph(id='pie-chart', style={'display': 'inline-block', 'width': '38%'})
    ]),

])

# Define the callback for the input field and button
@app.callback(
    [Output('line-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('variable-input', 'value')]
)

def update_graph(n_clicks, input_value):

    if n_clicks > 0 and input_value:
        
        # Filter data based on user input for line chart
        fin_city_line_df = fin_cities_df[fin_cities_df['Hinku calculation without emission credits'] == 'total emissions, ktCO2e']
        filtered_line_data = fin_city_line_df[fin_city_line_df['City'].str.contains(input_value, case=False)]
        
        # Filter data based on user input for pie chart
        exclude_terms = ['per person, tCO2e', 'population', 'total emissions, ktCO2e', 'Emission credits']
        fin_city_pie_df = fin_cities_df[fin_cities_df['Hinku calculation without emission credits'].isin(exclude_terms)]
        filtered_pie_data = fin_city_pie_df[fin_city_pie_df['City'].str.contains(input_value, case=False)]       

        # Line chart
        if not filtered_line_data.empty:
            # Convert the DataFrame from wide to long format for plotting
            # years = ['1990'] + [str(year) for year in range(2005, 2023)] # if you wanna add 1990, messed up x-scale though
            melted_line_data = filtered_line_data.melt(id_vars=['City'], value_vars=[str(year) for year in range(2005, 2023)],
                                             var_name='Year', value_name='Total Emissions (ktCO2e)')

            # Ensure the 'Year' column is numeric for plotting
            melted_line_data['Year'] = pd.to_numeric(melted_line_data['Year'])

            # Create a line chart
            fig_line = px.line(
                melted_line_data,
                x='Year',
                y='Total Emissions (ktCO2e)',
                title=f'Total Yearly Emissions for {input_value.capitalize()}'
            )
            fig_line.update_xaxes(
                tickmode='array',  # Define ticks manually
                tickvals=list(range(2005, 2023)),
                # tickangle=75
            )

        else:
            fig_line = {} # return empty figure
        
        # Pie chart
        if not filtered_pie_data.empty:
            
            emission_sources = [
                "Electricity", "Electric heating", "District heating", "Oil heating", "Other heating",
                "Industry", "Machinery", "Road transport", "Rail transport", "Water transport",
                "Agriculture", "Waste treatment", "F-gases"
                ]

            year = 2022 # this should be which year (2022 or 2030 or something else?)

            city_data = fin_cities_df[fin_cities_df['City'].str.contains(input_value, case=False, na=False)]

            pie_data = city_data[city_data['Hinku calculation without emission credits'].isin(emission_sources)]

            pie_chart_data = pie_data[['Hinku calculation without emission credits', str(year)]]
            pie_chart_data = pie_chart_data.groupby('Hinku calculation without emission credits')[str(year)].sum().reset_index()

            # Create a pie chart
            fig_pie = px.pie(
                pie_chart_data, values='2022',
                names='Hinku calculation without emission credits',
                hole=.5,
                title=f'Emissions by Sector in {input_value.capitalize()} in {year}'

            )
            fig_pie.update_traces(textinfo='none') # remove percentages from figure

        else:
            fig_pie = {} # return empty figure

        return fig_line, fig_pie # Always return figures
        
    # Default return when no input is provided or the conditions are not met
    return {}, {}


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

