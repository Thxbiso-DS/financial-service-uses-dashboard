import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from processing import load_and_clean_data, save_cleaned_data

pd.set_option('future.no_silent_downcasting', True)

input_file = "data/training.csv"
cleaned_data = load_and_clean_data(input_file)

output_file = "data/cleaned_training.csv"
save_cleaned_data(cleaned_data, output_file)

financial_services = [
    'Does not use any financial service',
    'Does not use mobile money',
    'Uses mobile money only',
    'Uses both'
]
income_columns = ['Salaries/wages', 'Trading/selling produce', 'Service providing income', 'Piece work/Casual labor',
                  'Rental income', 'Interest from savings/investments', 'Pension', 'Social welfare grant', 
                  'Expenses covered by others', 'Other income']

financial_service_options = [{'label': financial_service, 'value': financial_service} for financial_service in financial_services]
land_ownership_options = [{'label': land_owned, 'value': land_owned} for land_owned in cleaned_data['Ownership of land/plot'].unique()]
income_column_options = [{'label': column, 'value': column} for column in income_columns]


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Financial Services used in Tanzania"

app.layout = html.Div([
    html.Div([
        html.H1("Financial Services Uses in Tanzania", className="header-title"),
        html.P("A look at the different finanical services used across the country of Tanzania", className="header-description")
    ], className="Header"),

    html.Div([
        html.Label("Select Financial Service Category:", className="dropdown-label"),
        dcc.Dropdown(
            id='financial-service-dropdown',
            options=financial_service_options,
            value=financial_services[0],
            clearable=False,
            className="dropdown"
        ),
        dcc.Graph(id='financial-service-age-graph', className="graph"),

        html.Div([
            html.Div([
                html.Label("Select Financial Service Category for Gender Distribution:", className="dropdown-label"),
                dcc.Dropdown(
                    id='financial-service-gender-dropdown',
                    options=financial_service_options,
                    value=financial_services[0],
                    clearable=False,
                    className="dropdown"
                ),
                dcc.Graph(id="pie-chart-by-gender", className="graph")
            ], className="graph-container"),
            
            html.Div([
                html.Label("Select Financial Service Category for Marital Status Distribution:", className="dropdown-label"),
                dcc.Dropdown(
                    id='financial-service-marital-dropdown',
                    options=financial_service_options,
                    value=financial_services[0],
                    clearable=False,
                    className="dropdown"
                ),
                dcc.Graph(id="pie-chart-by-marital", className="graph")
            ], className="graph-container"),
        ]),

        html.Label("Select Financial Service Category for the Type of land ownership Distribution:", className="dropdown-label"),
        dcc.Dropdown(
            id='finanical-service-for-land-ownership',
            options=financial_service_options,
            value=financial_services[0],
            clearable=False,
            className="dropdown"
        ),
        dcc.Graph(id="land-owned-bar-graph", className="graph"),

        html.Label("Select Financial Service Category for Income Distribution:", className="dropdown-label"),
        dcc.Dropdown(
            id='financial-service-income-bar-dropdown',
            options=financial_service_options,
            value=financial_services[0],
            clearable=False,
            className="dropdown"
        ),
        dcc.Graph(id="income-category-bar-graph", className="graph"),

        html.Label("Select Income Category for Map Distribution:", className="dropdown-label"),
        dcc.Dropdown(
            id='income-column-dropdown',
            options=income_column_options,
            value=income_columns[0],
            clearable=False,
            className="dropdown"
        ),
        dcc.Graph(id="income-choropleth-map", className="graph")
    ], className="content")
])



@app.callback(
    [Output('financial-service-age-graph', 'figure'),
     Output('pie-chart-by-gender', 'figure'),
     Output('pie-chart-by-marital', 'figure'),
     Output('land-owned-bar-graph', 'figure'),
     Output('income-category-bar-graph', 'figure'),
     Output('income-choropleth-map', 'figure')],
    [Input('financial-service-dropdown', 'value'),
     Input('financial-service-gender-dropdown', 'value'),
     Input('financial-service-marital-dropdown', 'value'),
     Input('finanical-service-for-land-ownership', 'value'),
     Input('financial-service-income-bar-dropdown', 'value'),
     Input('income-column-dropdown', 'value')]
)


def update_graphs(selected_category, gender_category, marital_category, land_ownership_category, income_category, selected_income_column):
    
    
    filtered_data = cleaned_data[cleaned_data['Mobile money classification'] == selected_category]
    grouped_data = filtered_data.groupby(['Age', 'Mobile money classification']).size().reset_index(name='User Count')
    age_chart = px.scatter(grouped_data, x='Age', y='User Count', color='Mobile money classification',
                           title=f"Number of Users per Age Group for the <br>Mobile Money Classification: '{selected_category}'",
                           labels={'Age': 'Age of users', 'User Count': 'Number of Users', 'Mobile money classification': 'Mobile Money Classification'})
    age_chart.update_layout(legend_title_text='Mobile Money Classification',
                            title={'font': {'size': 24, 'family': 'Arial', 'weight': 'bold'}},
                            xaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                            yaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                            legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})
    age_chart.update_traces(hovertemplate='Age: %{x}<br>Number of Users: %{y}')

    gender_data = cleaned_data[cleaned_data['Mobile money classification'] == gender_category]
    gender_pie_chart = px.pie(gender_data, names='Gender', 
                              title=f"Gender Distribution for the Mobile Money Classification: '{gender_category}'")
    gender_pie_chart.update_layout(legend_title_text='Gender',
                                   title={'font': {'size': 20, 'family': 'Arial', 'weight': 'bold'}},
                                   legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})
    gender_pie_chart.update_traces(hovertemplate='Gender: %{label}<extra></extra>')
    
    marital_data = cleaned_data[cleaned_data['Mobile money classification'] == marital_category]
    marital_pie_chart = px.pie(marital_data, names='Marital status', 
                               title=f"Marital Status Distribution for the Mobile Money Classification: '{marital_category}'")
    marital_pie_chart.update_layout(legend_title_text='Marital Status',
                                    title={'font': {'size': 20, 'family': 'Arial', 'weight': 'bold'}},
                                    legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})
    marital_pie_chart.update_traces(hovertemplate='Marital Status: %{label}<extra></extra>')

    
    land_data = cleaned_data[cleaned_data['Mobile money classification'] == land_ownership_category]
    grouped_land_data = land_data.groupby(['Ownership of land/plot', 'Mobile money classification']).size().reset_index(name='User Count')
    land_ownership_bar = px.bar(grouped_land_data, x='Ownership of land/plot', y='User Count', color='Mobile money classification',
                                title=f"Land Ownership Distribution for the <br>Mobile Money Classification: '{land_ownership_category}' ",
                                labels={'Ownership of land/plot': 'Land Ownership', 'User Count': 'Number of Users', 'Mobile money classification': 'Mobile Money Classification'})
    land_ownership_bar.update_layout(title={'font': {'size': 24, 'family': 'Arial', 'weight': 'bold'}},
                                    xaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                                    yaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                                    legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})
    land_ownership_bar.update_traces(hovertemplate='Land status: %{label}<extra></extra>')

 
    filtered_income_data = cleaned_data[income_columns + ['Mobile money classification']].copy()
    filtered_income_data.replace({'Yes': 1, 'No': 0}, inplace=True)
    grouped_income_data = filtered_income_data.groupby(['Mobile money classification']).sum()
    grouped_income_data_transposed = grouped_income_data.transpose().reset_index()
    income_category_bar = px.bar(grouped_income_data_transposed, x='index', y=income_category, 
                                 title=f"Income Category Distribution for the <br>Mobile Money Classification:'{income_category}'",
                                 labels={'index': 'Income Category', income_category: 'Number of Users'})
    income_category_bar.update_layout(legend_title_text='Mobile Money Classification',
                                      title={'font': {'size': 24, 'family': 'Arial', 'weight': 'bold'}},
                                      xaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                                      yaxis_title={'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}},
                                      legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})
    income_category_bar.update_traces(hovertemplate='Income catergory: %{x}<br>Number of users: %{y}')

    income_filtered_data = cleaned_data[cleaned_data[selected_income_column] == 'Yes']
    income_map_distribution = px.scatter_mapbox(
        income_filtered_data, 
        lat='Latitude', 
        lon='Longitude',
        color='Mobile money classification',  
        hover_data={'Latitude': True, 'Longitude': True}, 
        mapbox_style="carto-positron", 
        zoom=5,  
        center={"lat": -6.369028, "lon": 34.888822},  
        title=f"Income Distribution for {selected_income_column}"
    ) 
    income_map_distribution.update_traces(hovertemplate='Mobile Money Classification: %{text}<extra></extra>',
                                          text=income_filtered_data['Mobile money classification'],
                                          marker=dict(size=8.5, opacity=0.7))     
    income_map_distribution.update_layout(legend_title_text='Mobile Money Classification',
                                          margin={"r":0,"t":0,"l":0,"b":0},
                                          legend_title={'font': {'size': 14, 'family': 'Arial', 'weight': 'bold'}})   

    return age_chart, gender_pie_chart, marital_pie_chart, land_ownership_bar, income_category_bar, income_map_distribution

if __name__ == '__main__':
    app.run_server(debug=True)