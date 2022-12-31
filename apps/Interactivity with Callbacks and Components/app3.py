import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
logo_link = '../../data/external/e_com_logo.png'
# logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'

app = dash.Dash(__name__)

app.layout = html.Div([
  html.Img(src=app.get_asset_url("e_com_logo.png"),style={'margin':'30px 0px 0px 0px' }),
  html.H1('Sales breakdowns'),
  html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Controls'),
        html.Br(),
        html.H3('Country Select'),
        dcc.Dropdown(id='country_dd',
        options=[
            {'label':'UK', 'value':'United Kingdom'},
            {'label':'GM', 'value':'Germany'},
            {'label':'FR', 'value':'France'},
            {'label':'AUS', 'value':'Australia'},
            {'label':'HK', 'value':'Hong Kong'}],
            style={'width':'200px', 'margin':'0 auto'})
        ],
        style={'width':'350px', 'height':'350px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
    html.Div(children=[
            dcc.Graph(id='major_cat'),
            html.H2('Major Category', 
            style={ 'border':'2px solid black', 'width':'200px', 'margin':'0 auto'})
            ],
             style={'width':'700px','display':'inline-block'}
             ),
    ])], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
  )
@app.callback(
    Output(component_id='major_cat', component_property='figure'),
    Input(component_id='country_dd', component_property='value')
)

def update_plot(input_country):
    # Set a default value
    country_filter = 'All Countries'
    # Ensure the DataFrame is not overwritten
    sales = ecom_sales.copy(deep=True)
    # Create a conditional to filter the DataFrame if the input exists
    if input_country:
        country_filter = input_country
        sales = sales[sales['Country'] == country_filter]
    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    bar_fig_major_cat = px.bar(
        title=f'Sales in {country_filter}', data_frame=ecom_bar_major_cat, x='Total Sales ($)', y='Major Category', color='Major Category',
                 color_discrete_map={'Clothes':'blue','Kitchen':'red','Garden':'green','Household':'yellow'})
   	# Return the figure
    return bar_fig_major_cat


if __name__ == '__main__':
    app.run_server(debug=True)