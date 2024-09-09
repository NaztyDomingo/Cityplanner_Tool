import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import visualization_data as vd
import dataframe_helper as dh
import database_puller as dp

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Dash Data Visualization"

# Load and unpack dfs from database
dfs = dp.pull_all()
# dfs = vd.load_data()
# print(len(dfs))
fin_cities_df, fin_regions_df, agriculture_fin_df, air_passenger_and_cargo_transport_fin_df, supplementary_data_fin_df, energy_consumption_and_population_fin_df, energy_agric_fin_df, transportation_fin_df, swe_cities_df, swe_regions_df, avg_co2_consumption_df, final_tree_info_df, partial_tree_info_df = dfs

# Modify dfs
final_tree_info_df.drop(columns=['Maintenance'], inplace=True)
final_tree_info_df.rename(columns={'Average_heigh_range_m': 'Average Height (m)'})

combine_list = [fin_cities_df, swe_cities_df]
combined_cities_df = pd.concat(combine_list)

# Define the layout and style of the app
app.layout = html.Div([

    html.H1(
        "Cityplanner Tool",
        style={
            'textAlign': 'center',
                        'fontFamily': 'Open Sans, verdana, arial, sans-serif'
        }),
    
    # Input and Button
    html.Div(
        style={
            'display': 'flex',
            'justifyContent': 'center',  
            'alignItems': 'center',      
            'margin': '20px',
                        'fontFamily': 'Open Sans, verdana, arial, sans-serif'             
        },
        children=[
            dcc.Input(
                id='variable-input',
                type='text',
                placeholder='Enter a city',
                style={
                    'width': '400px',
                    'height': '50px',
                    'fontSize': '18px'
                }
            ),
            html.Button(
                'Submit',
                id='submit-button',
                n_clicks=0,
                style={
                    'height': '50px',
                    'fontSize': '18px',
                    'padding': '10px 20px',
                    'marginLeft': '10px',
                    #'background-color': '#d3dcd5'
                }
            )
        ]
    ),
    
    # Container for the two graphs side by side
    html.Div([
        # Line chart for emissions over years
        dcc.Graph(id='line-or-bar-chart', style={'display': 'inline-block', 'width': '68%', 'height': '500px'}),
        
        # Pie chart for emissions by source
        dcc.Graph(id='pie-chart', style={'display': 'inline-block', 'width': '32%', 'height': '500px'}),

    # Tree data table
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in final_tree_info_df.columns],
        data=final_tree_info_df.to_dict('records'),
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'left',
            'fontFamily': 'Open Sans, verdana, arial, sans-serif',
            'fontSize': '14px'
        },
        style_header={
            'backgroundColor': '#d3dcd5',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }],
        page_size=10)
    ]),
])

# Define the callback for the input field and button
@app.callback(
    [Output('line-or-bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('variable-input', 'value')]
)

def update_graph(n_clicks, input_value):
    
    emission_sources = [
                'Waste And Sewage', 'Machinery', 'Electricity And District Heating',
                'Other Heating', 'Agriculture', 'Transportation','Industry'
                ]

    # TODO: fix color palette and make it work with default graphs, add default order in legend
    color_palette = {
    "Electricity": "#1f77b4",
    "Electric heating": "#ff7f0e",
    "District heating": "#2ca02c",
    "Oil heating": "#d62728",
    "Other heating": "#9467bd",
    "Industry": "#8c564b",
    "Machinery": "#e377c2",
    "Road transport": "#7f7f7f",
    "Rail transport": "#bcbd22",
    "Water transport": "#17becf",
    "Agriculture": "#aec7e8",
    "Waste treatment": "#ffbb78",
    "F-gases": "#98df8a"
    }

    # Default view for the page = User has not entered search parameters
    if n_clicks == 0 or not input_value:

        # Filter the DataFrame to only include relevant emission sources
        filtered_df = fin_regions_df[fin_regions_df['Year'] == 2022][['Region'] + emission_sources]
        
        # For default stacked bar chart for Finland
        # Pivot the DataFrame to have Regions as index and emission sources as columns
        pivot_df = filtered_df.set_index('Region')

        # Add traces to bar chart for each emission source and update layout
        fig_bar = go.Figure()
        for emission_source in emission_sources:
            if emission_source in pivot_df.columns:
                fig_bar.add_trace(go.Bar(
                    x=pivot_df.index,
                    y=pivot_df[emission_source],
                    name=emission_source,
                    #marker_color=color_palette[emission_sources] # not working
                ))
        fig_bar.update_layout(
            barmode='stack',
            xaxis_title='Region',
            yaxis_title='Total Emissions in 2022 (kt CO2e)',
            title='Total Emissions by Region and Source in Finland (2022)',
        )

        # For default pie chart for Finland
        aggregated_df = filtered_df[emission_sources].sum().reset_index()
        aggregated_df.columns = ['Hinku calculation without emission credits', 'Total Emissions 2022']

        fig_pie = px.pie(
            aggregated_df,
            values='Total Emissions 2022',
            names='Hinku calculation without emission credits',
            hole=.5,
            title='Total Emissions by Source in Finland (2022)'
        )
        fig_pie.update_traces(textinfo='none') # remove percentages from figure

        return fig_bar, fig_pie
    
        # TODO: Add two charts for default Sweden data?
        # Also consider how will that effect the overall layout (N of outputs)

    # User has entered a search parameter
    if n_clicks > 0 and input_value:

        # Create new column with special character versions of city names (SWE and FIN cities)
        combined_cities_df['City With Special Characters'] = combined_cities_df['City'].apply(dh.reverse_special_chars_finish)
        
        # Filter data based on user input for line chart
        filtered_line_data = combined_cities_df[combined_cities_df['City With Special Characters'].str.contains(input_value, case=False)]
        
        # Line chart
        if not filtered_line_data.empty:

            # Ensure the 'Year' column is treated as a string (categorical data) to have equally spaced x-axis
            filtered_line_data['Year'] = filtered_line_data['Year'].astype(str)

            # Create a line chart using Year and Total Emissions
            fig_line = px.line(
                filtered_line_data,
                x='Year',
                y='Total Emissions',
                title=f'Total Yearly Emissions for {input_value.capitalize()}',
                category_orders={'Year': sorted(filtered_line_data['Year'].unique(), key=lambda x: int(x))}  # Ensures years are sorted correctly
            )
            fig_line.update_xaxes(
                type='category',  # Treat 'Year' as a category
                #tickangle=75
            )
        else:
            fig_line = {} # return empty figure
        
        # Filter data based on user input for pie chart
        filtered_pie_data = combined_cities_df[
            (combined_cities_df['City With Special Characters'].str.contains(input_value, case=False)) &
            (combined_cities_df['Year'] == 2022)
        ]

        # Pie chart
        if not filtered_pie_data.empty:

            # Prepare data for pie chart
            pie_chart_data = filtered_pie_data[emission_sources].melt(var_name='Source', value_name='Emissions')
            pie_chart_data = pie_chart_data.groupby('Source')['Emissions'].sum().reset_index()

            ## Create a pie chart
            fig_pie = px.pie(
                pie_chart_data,
                values='Emissions',
                names='Source',
                hole=.5,
                title=f'Emissions by Sector in {input_value.capitalize()} in 2022'
            )
            fig_pie.update_traces(textinfo='none') # remove percentages from figure

        else:
            fig_pie = {} # return empty figure

        return fig_line, fig_pie # Always return figures
        
    # Default return when no input is provided
    return {}, {}

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

