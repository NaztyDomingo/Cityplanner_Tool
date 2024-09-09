import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import visualization_data as vd

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Dash Data Visualization"

# Load and unpack dfs
dfs = vd.load_data()
fin_cities_df, fin_regions_df, tree_df = dfs

# modify tree_df to fit table better
tree_df.drop(columns=['Maintenance'], inplace=True)

# Define the layout of the app
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

    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in tree_df.columns],
        data=tree_df.to_dict('records'),
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
            }
        ],
        page_size=10
    )
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
                "Electricity", "Electric heating", "District heating", "Oil heating", "Other heating",
                "Industry", "Machinery", "Road transport", "Rail transport", "Water transport",
                "Agriculture", "Waste treatment", "F-gases"
                ]
    
    # TODO: fix color palette and make it work with default graphs
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

    if n_clicks == 0 or not input_value:

        # Filter the DataFrame to only include relevant emission sources
        filtered_df = fin_regions_df[fin_regions_df['Hinku calculation without emission credits'].isin(emission_sources)]

        # For default stacked bar chart for Finland
        # Pivot the DataFrame to have Regions as index and emission sources as columns
        pivot_df = filtered_df.pivot_table(
            index='Region',
            columns='Hinku calculation without emission credits',
            values='Total emissions2022(kt CO2e)',
            aggfunc='sum'
        ).fillna(0)

        fig_bar = go.Figure()

        # Add traces for each emission source, update layout and show figure
        for emission_source in emission_sources:
            if emission_source in pivot_df.columns:
                fig_bar.add_trace(go.Bar(
                    x=pivot_df.index,
                    y=pivot_df[emission_source],
                    name=emission_source,
                    #marker_color=color_palette[emission_source]
                ))
        fig_bar.update_layout(
            barmode='stack',
            xaxis_title='Region',
            yaxis_title='Total Emissions in 2022 (kt CO2e)',
            title='Total Emissions by Region and Source in Finland (2022)',
        )

        # For default pie chart for Finland
        aggregated_df = filtered_df.groupby('Hinku calculation without emission credits')['Total emissions2022(kt CO2e)'].sum().reset_index()
        fig_pie = px.pie(
            aggregated_df,
            values='Total emissions2022(kt CO2e)',
            names='Hinku calculation without emission credits',
            # color_discrete_sequence=[color_palette[source] for source in emission_sources],
            hole=.5,
            title='Total Emissions by Source in Finland (2022)'
        )
        fig_pie.update_traces(textinfo='none') # remove percentages from figure

        return fig_bar, fig_pie
    
        # TODO: Add two charts for default Sweden data?
        # Also consider how will that effect the overall layout (N of outputs)

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

            year = 2022 # TODO: Change year? (2022 or 2030 or something else?)

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

