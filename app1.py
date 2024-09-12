import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import visualization_data as vd
import dataframe_helper as dh
import database_puller as dp
import graph_display as gd
import tree_calc as tc


def main():
    # Initialize the Dash app
    app = dash.Dash(__name__)
    app.title = "Dash Data Visualization"

    # Load and unpack dfs from database
    dfs = dp.pull_all()
    # dfs = vd.load_data()
    # print(len(dfs))
    # fin_cities_df, fin_regions_df, fin_city_predictions, fin_region_predictions, swe_city_predictions, agriculture_fin_df, air_passenger_and_cargo_transport_fin_df, supplementary_data_fin_df, energy_consumption_and_population_fin_df, energy_agric_fin_df, transportation_fin_df, swe_cities_df, swe_regions_df, avg_co2_consumption_df, final_tree_info_df, partial_tree_info_df, = dfs
    fin_cities_df, fin_regions_df, agriculture_fin_df, air_passenger_and_cargo_transport_fin_df, supplementary_data_fin_df, energy_consumption_and_population_fin_df, energy_agric_fin_df, transportation_fin_df, swe_cities_df, swe_regions_df, avg_co2_consumption_df, final_tree_info_df, partial_tree_info_df, = dfs

    # Modify dfs
    final_tree_info_df.drop(columns=['Maintenance'], inplace=True)
    final_tree_info_df.rename(
        columns={'Average_heigh_range_m': 'Average Height (m)'})

    combine_list = [fin_cities_df, swe_cities_df]
    combined_cities_df = pd.concat(combine_list)
    # print(combined_cities_df)

    # Define the layout and style of the app
    app_layout(final_tree_info_df, app)

    # callback + func to dynamically change title
    @app.callback(
        Output('dynamic-title', 'children'),
        [Input('country-dropdown', 'value')]
    )
    def update_title(country_selection):
        return f'Total Emissions by Region and Source in {country_selection} (2022)'

    # Define the callback for the input field and button
    @app.callback(
        [Output('line-or-bar-chart', 'figure'), Output('pie-chart', 'figure'),
         Output('recommendations-bar-chart', 'figure')],
        # , Output('line-or-bar-chart', 'style'), Output('pie-chart', 'style')
        [Input('country-dropdown', 'value'),
         Input('submit-button', 'n_clicks'),
         Input('year-slider', 'value')],
        [State('variable-input', 'value')]
    )
    def update_graph(country_selection, n_clicks, selected_year, input_value):

        emission_sources = [
            'Waste And Sewage', 'Machinery', 'Electricity And District Heating',
            'Other Heating', 'Agriculture', 'Transportation', 'Industry'
        ]

        # Default view for the page = User has not entered search parameters
        if not input_value:
            # Filter the DataFrame to only include relevant emission sources. Country determined by dropdown
            if 'Finland' in country_selection:
                filtered_df = fin_regions_df[fin_regions_df['Year'] == 2022][[
                    'Region'] + emission_sources]
            else:
                filtered_df = swe_regions_df[swe_regions_df['Year'] == 2022][[
                    'Region'] + emission_sources]

            # For default stacked bar chart for
            # Pivot the DataFrame to have Regions as index and emission sources as columns
            pivot_df = filtered_df.set_index('Region')

            # Add traces to bar chart for each emission source and update layout
            fig_bar = go.Figure()
            fig_bar = gd.bar(pivot_df, fig_bar)

            # For default pie chart for Finland
            aggregated_df = filtered_df[emission_sources].sum().reset_index()
            aggregated_df.columns = [
                'Hinku calculation without emission credits', 'Total Emissions 2022']

            fig_pie = go.Figure()
            fig_pie = gd.pie(aggregated_df, fig_pie)

            # Default tree CO2 consumption bar chart
            fig_rec = go.Figure()
            fig_rec = gd.tree_co2(final_tree_info_df, fig_rec)

            return fig_bar, fig_pie, fig_rec

        # User has entered a search parameter
        if input_value:

            inputted_styles1 = inputted1_graph_style
            inputted_styles2 = inputted2_graph_style

            # Create new column with special character versions of city names (SWE and FIN cities)
            combined_cities_df['City With Special Characters'] = combined_cities_df['City'].apply(
                dh.reverse_special_chars_finish)

            # Filter data based on user input for line chart
            filtered_line_data = combined_cities_df[combined_cities_df['City With Special Characters'].str.contains(
                input_value, case=False)]

            # Line chart
            if not filtered_line_data.empty:

                # Ensure the 'Year' column is treated as a string (categorical data) to have equally spaced x-axis
                filtered_line_data['Year'] = filtered_line_data['Year'].astype(
                    str)

                predicted_df = dp.pull_predictions(input_value)

                # Create a line chart using Year and Total Emissions
                fig_line = go.Figure()
                fig_line = gd.line(predicted_df, input_value, fig_line)

            else:
                fig_line = {}  # return empty figure

            # Filter data based on user input for pie chart
            filtered_pie_data = combined_cities_df[
                (combined_cities_df['City With Special Characters'].str.contains(input_value, case=False)) &
                (combined_cities_df['Year'] == 2022)
            ]

            # Pie chart
            if not filtered_pie_data.empty:

                # Prepare data for pie chart
                pie_chart_data = filtered_pie_data[emission_sources].melt(
                    var_name='Source', value_name='Emissions')
                pie_chart_data = pie_chart_data.groupby(
                    'Source')['Emissions'].sum().reset_index()

                # Create a pie chart
                fig_pie = go.Figure()
                fig_pie = gd.pie_city(pie_chart_data, input_value, fig_pie)

            else:
                fig_pie = {}  # return empty figure

            predicted_df = dp.pull_predictions(input_value)

            # Filter data based on user input for tree recommendations chart
            filtered_rec_data = tc.calc_trees(
                combined_cities_df, final_tree_info_df, predicted_df, str(selected_year), input_value)
            # print(combined_cities_df)

            # Tree recommendations
            if not filtered_rec_data.empty:

                # Create a tree recommendations chart
                fig_rec = go.Figure()
                fig_rec = gd.tree_rec(filtered_rec_data, input_value, fig_rec)

            else:
                fig_rec = {}  # return empty figure

            return fig_line, fig_pie, fig_rec  # , inputted_styles1, inputted_styles2

        # Default return when no input is provided
        return {}, {}, {}  # , {}, {} # empty returns for the styling elements

    # @app.callback(
    #     Output('country-dropdown', 'style'),
    #     [Input('submit-button', 'n_clicks')]
    # )
    # def toggle_dropdown(n_clicks):
    #     #hide the dropdown when entering a city (if n_clicks is greater than 0)
    #     if n_clicks > 0:
    #         return {'display': 'none'}
    #     return {'display': 'block'}

    # callback used for dropdown visibility
    @app.callback(
        Output('div-to-toggle', 'style'),
        [Input('submit-button', 'n_clicks')],
        [State('variable-input', 'value')]
    )
    # func used for dropdown visibility
    def toggle_dropdown(n_clicks, input_value):

        # if no input, show
        if not input_value:
            return {'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px', 'width': '100%'}

        # hide if the button has been clicked and input is provided
        if n_clicks > 0:
            return {'display': 'none'}

        # default: show
        return {'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin': '20px', 'width': '100%'}

    ##### ALWAYS HIDES SLIDER ####
    @app.callback(
        Output('slider-container', 'style'),
        [Input('submit-button', 'n_clicks')],
        [State('variable-input', 'value')]
    )
    def toggle_slider_visibility(n_clicks, input_value):

        if input_value:
            return {'display': 'none'}
            #return {'display': 'block', 'width': '80%', 'marginLeft': '10%'}

        return {'display': 'none'}

    app.run_server(debug=True)


def app_layout(df, app: dash.Dash) -> None:
    app.layout = init_app(df)


def init_app(df) -> html.Div:
    init_layout = []

    init_layout = html.Div([

        html.H1(
            "Cityplanner Tool",
            style=h1_graph_style),

        # Input and Button
        html.Div(
            style=div_graph_style,
            children=[
                dcc.Input(
                    id='variable-input',
                    type='text',
                    placeholder='Enter a city',
                    style=children_graph_style
                ),
                html.Button(
                    'Submit',
                    id='submit-button',
                    n_clicks=0,
                    style=button_graph_style
                )
            ]
        ),

        # Checklist for country selection
        html.Div(
            id='div-to-toggle',
            style=div_graph_style,
            children=[
                html.Div(
                    html.H3(
                        id='dynamic-title',
                        children='Total Emissions by Region and Source in <country> (2022)'
                    ),
                    style=nested_title_div
                ),
                html.Div(
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=['Finland', 'Sweden'],
                        value='Finland',
                        clearable=False,
                        style={'textAlign': 'center', 'width': '250px'}
                    ),
                    style=nested_dropdown_div
                ),
            ]
        ),

        # Main (stacked)bar chart
        html.Div([
            # Line chart for emissions over years
            dcc.Graph(id='line-or-bar-chart', style=default1_graph_style),


            # Container for the two graphs side by side
            html.Div([
                # Pie chart for emissions by source
                dcc.Graph(id='recommendations-bar-chart', style=style_rec1),
                dcc.Graph(id='pie-chart', style=default2_graph_style),
            ],
                style=style_rec_div),

            # Slider for selecting year
            html.Div(
                id='slider-container',  # Add an ID to the wrapper Div
                children=[
                    dcc.Slider(
                        id='year-slider',
                        min=2022,
                        max=2025,
                        step=1,
                        value=2022,
                        marks={year: {'label':str(year), 'style': {'fontSize': '16px', 'fontFamily': 'Open Sans, verdana, arial, sans-serif'}} for year in range(2022, 2026)},
                    ),
                ],
                style=slider_div_style
            ),

            # Tree data table
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell=style_cell,
                style_header=style_header,
                style_data_conditional=style_data_conditional,
                page_size=10)
        ]),
    ])

    return init_layout


# TODO: styles modularize
h1_graph_style = {
    'textAlign': 'center',
    'fontFamily': 'Open Sans, verdana, arial, sans-serif'
}

nested_title_div = {
    'width': '650px',
    # 'margin-right': '15px'
    'fontFamily': 'Open Sans, verdana, arial, sans-serif',
}

nested_dropdown_div = {
    'width': '250px',
    # 'margin-left': '15px'
    'fontFamily': 'Open Sans, verdana, arial, sans-serif',
}

div_graph_style = {
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'center',
    'margin': '20px',
    'fontFamily': 'Open Sans, verdana, arial, sans-serif',
    'width': '100%'
}

children_graph_style = {
    'width': '400px',
    'height': '50px',
    'fontSize': '18px',
    'paddingLeft': '10px',
    'borderRadius': '4px'
}

button_graph_style = {
    'height': '50px',
    'fontSize': '18px',
    'padding': '10px 20px',
    'marginLeft': '10px',
    'background-color': '#a7d2ac',
    'border': '0px',
    'border-radius': '4px',
    # 'background-color': '#d3dcd5'
}


style_rec1 = {'display': 'inline-block', 'width': '68%', 'height': '500px'}
style_rec_div = {'marginTop': '30px'}
slider_div_style = {'width': '80%', 'marginLeft': '10%'} 


default1_graph_style = {'display': 'inline-block',
                        'width': '100%', 'height': '750px'}
default2_graph_style = {'display': 'inline-block',
                        'width': '32%', 'height': '500px'}

inputted1_graph_style = {'display': 'inline-block',
                         'width': '40%', 'height': '500px'}
inputted2_graph_style = {'display': 'inline-block',
                         'width': '60%', 'height': '500px'}

style_cell = {
    'whiteSpace': 'normal',
    'height': 'auto',
    'textAlign': 'left',
    'fontFamily': 'Open Sans, verdana, arial, sans-serif',
    'padding': '10px',
    'fontSize': '14px'
}
style_header = {
    'marginTop': '10px',
    'backgroundColor': '#a7d2ac',
    'color': '#000000',
    'fontWeight': 'bold'
}
style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }]

# Run app
if __name__ == '__main__':
    main()
