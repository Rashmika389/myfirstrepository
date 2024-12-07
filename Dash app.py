# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options=[{'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}]
        
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                style={'textAlign': 'center', 'color': '#503D36',
                        'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        html.Div([
                html.Label("Select Launch Site:"),
                dcc.Dropdown(
                    id='site-dropdown',
                    options=options,
                    value='ALL',
                    placeholder='Select a Launch Site',
                    searchable=True
                )]),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload]
            ),
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data=filtered_df.groupby('Launch Site')['class'].count()
        fig = px.pie(data, values=data.values, 
        names=data.index, 
        title='Total Success Launches By Site')
        return fig
    else:
        data=filtered_df[filtered_df['Launch Site']==entered_site]['class'].value_counts()
        fig = px.pie(data, values=data.values, 
        names=data.index, 
        title=f'Total Success Launches for site {entered_site}')
        return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown','value'), 
    Input("payload-slider", "value")]
)

def get_scatter_chart(entered_site,payload):
    filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site)]
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x="Payload Mass (kg)", 
        y="class", 
        title='Correlation between Payload and success for all Sites',
        color='Booster Version Category')
        return fig
    else:
        data=filtered_df[((filtered_df['Payload Mass (kg)']>= payload[0]) & (filtered_df['Payload Mass (kg)']<= payload[1]))]
        fig = px.scatter(data, x="Payload Mass (kg)", 
        y="class", 
        title=f'Correlation between Payload and success for the Site {entered_site}',
        color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)