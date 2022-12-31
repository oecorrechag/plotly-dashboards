import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, date
ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
logo_link = '../../data/external/e-comlogo.png'
# logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
ecom_sales['InvoiceDate'] = pd.to_datetime(ecom_sales['InvoiceDate'])

app = dash.Dash(__name__)

def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

def add_logo():
    corp_logo = html.Img(
        src=app.get_asset_url("e-comlogo.png"),
        style={'margin':'20px 20px 5px 5px',
              'border':'1px dashed lightblue',
              'display':'inline-block'})
    return corp_logo

# Create a function to add corporate styling
def style_c():
    layout_style={'display':'inline-block','margin':'0 auto','padding':'20px'}
    return layout_style

app.layout = html.Div([
  add_logo(),
  *make_break(2),
  html.H1('Sales Dashboard'),
  *make_break(3),
  html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Controls', style=style_c()),
        html.H3('Search Descriptions'),
        *make_break(2),
        # Add the required input
        dcc.Input(id='search_desc', type='text', placeholder ='Filter Product Descriptions',
        # Ensure input is triggered with 'Enter'
        debounce=True,
        # Ensure the plot can load without a selection
        required=False,
        style={'width':'200px', 'height':'30px'})
        ],
        style={'width':'350px', 'height':'350px', 'vertical-align':'top', 'border':'1px solid black',
        'display':'inline-block', 'margin':'0px 80px'}),
    html.Div(children=[
            dcc.Graph(id='sales_desc'),
            html.H2('Sales Quantity by Country', 
            style={ 'border':'2px solid black', 'width':'400px', 'margin':'0 auto'})
            ],
             style={'width':'700px','display':'inline-block'}
             ),
    ])
    ], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
  )

@app.callback(
    Output(component_id='sales_desc', component_property='figure'),
    Input(component_id='search_desc', component_property='value')
)
def update_plot(search_value):
    title_value = 'None Selected (Showing all)'

    sales = ecom_sales.copy(deep=True)

    # Undertake the filter here using the user input
    if search_value:
        sales = sales[sales['Description'].str.contains(search_value, case=False)]
        title_value = search_value

    fig = px.scatter(data_frame=sales, 
                    y='OrderValue', x='Quantity', color='Country',title=f'Sales with description text: {title_value}')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)