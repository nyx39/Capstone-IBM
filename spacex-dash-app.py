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
launch_sites = spacex_df['Launch Site'].unique()
#print(launch_sites)
opt=[{'label': 'All Sites', 'value': 'ALL'}]
for elem in launch_sites:
    opt.append({'label': elem, 'value': elem})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=opt, value='ALL', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site').agg(
            counts = ('Launch Site', 'count')).reset_index()
        fig = px.pie(filtered_df, values='counts', names="Launch Site")
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]['class'].reset_index()
        df_class= filtered_df.groupby('class').agg(
            counts = ('class', 'count')
        ).reset_index()
        fig = px.pie(df_class, values='counts', names='class')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")
)
def boosters(entered_site, slider):
    low, high = slider
    if entered_site=='ALL':
        filter = (spacex_df['Payload Mass (kg)']> low) & (spacex_df['Payload Mass (kg)']< high)
        fig = px.scatter(spacex_df[filter], x='Payload Mass (kg)', y='class', color="Booster Version Category" )
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site].reset_index()
        filter = (filtered_df['Payload Mass (kg)']> low) & (filtered_df['Payload Mass (kg)']< high)
        fig = px.scatter(filtered_df[filter], x='Payload Mass (kg)', y='class', color="Booster Version Category" )
        return fig
        pass



# Run the app
if __name__ == '__main__':
    app.run()
