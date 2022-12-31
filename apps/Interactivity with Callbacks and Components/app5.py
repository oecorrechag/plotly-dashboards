import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, date

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
ecom_sales['InvoiceDate'] = pd.to_datetime(ecom_sales['InvoiceDate'])
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
        html.H3('Sale Date Select'),
        # Create a single date picker with identifier
        dcc.DatePickerSingle(id='sale_date',
            # Set the min/max dates allowed as the min/max dates in the DataFrame
            min_date_allowed=ecom_sales['InvoiceDate'].min(),
            max_date_allowed=ecom_sales['InvoiceDate'].max(),
            # Set the initial visible date
            date=date(2011,4,11),
            initial_visible_month=date(2011,4,11),
            style={'width':'200px', 'margin':'0 auto'})
        ],
        style={'width':'350px', 'height':'350px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
    html.Div(children=[
      		# Add a component to render a Plotly figure with the specified id
            dcc.Graph(id='sales_cat'),
            html.H2('Daily Sales by Major Category', 
            style={ 'border':'2px solid black', 'width':'400px', 'margin':'0 auto'})
            ],
             style={'width':'700px','display':'inline-block'}
             ),
    ]),
    ], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
  )

@app.callback(
    Output(component_id='sales_cat', component_property='figure'),
    Input(component_id='sale_date', component_property='date')
)
def update_plot(input_date):
    
    sales = ecom_sales.copy(deep=True)
    if input_date:
        sales = sales[sales['InvoiceDate'] == input_date]
        
    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    bar_fig_major_cat = px.bar(
        title=f'Sales on: {input_date}',data_frame=ecom_bar_major_cat, orientation='h', 
        x='Total Sales ($)', y='Major Category')

    return bar_fig_major_cat


if __name__ == '__main__':
    app.run_server(debug=True)