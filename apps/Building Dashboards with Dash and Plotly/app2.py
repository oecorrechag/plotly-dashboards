import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
logo_link = '../../data/external/e-comlogo.png'
ecom_country = ecom_sales.groupby('Country')['OrderValue'].agg(['sum', 'count']).reset_index().rename(columns={'count':'Sales Volume', 'sum':'Total Sales ($)'})

ecom_sales['InvoiceDate'] = pd.to_datetime(ecom_sales['InvoiceDate'])

# Add the country data to the scatter plot
ecom_scatter = px.scatter(ecom_country, x='Total Sales ($)', y='Sales Volume', 
                          color='Country', width=350, height=400, custom_data=['Country'])
ecom_scatter.update_layout({'legend':dict(orientation='h', y=-0.5,x=1, yanchor='bottom', xanchor='right'), 'margin':dict(l=20, r=20, t=25, b=0)})

app = dash.Dash(__name__)

app.layout = html.Div([
  html.Img(src=app.get_asset_url("e-comlogo.png"),
        style={'margin':'30px 0px 0px 0px' }),
  html.H1('Sales breakdowns'),
  html.Div(
    children=[
    html.Div(
        children=[
          html.H2('Sales by Country'),
          dcc.Graph(id='scatter_fig', figure=ecom_scatter)
        ],
        style={'width':'350px', 'height':'500px', 'display':'inline-block', 
               'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
    html.Div(
        children=[
          html.H2('Key Stats'),
          html.P(id='text_output', style={'width':'500px', 'text-align':'center'}),
          ],
          style={'width':'700px', 'height':'650px','display':'inline-block'}),
    ]),], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'})

# Trigger callback on hover
@app.callback(
    Output('text_output', 'children'),
    Input('scatter_fig', 'hoverData'))

def get_key_stats(hoverData):
    
    if not hoverData:
        return 'Hover over a country to see key stats'
	
    # Extract the custom data from the hoverData
    country = hoverData['points'][0]['customdata'][0]
    country_df = ecom_sales[ecom_sales['Country'] == country]
    
    top_major_cat = country_df.groupby('Major Category').agg('size').reset_index(name='Sales Volume').sort_values(by='Sales Volume', ascending=False).reset_index(drop=True).loc[0,'Major Category']
    top_sales_month = country_df.groupby('Year-Month')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)').sort_values(by='Total Sales ($)', ascending=False).reset_index(drop=True).loc[0,'Year-Month']
	
    # Use the aggregated variables
    stats_list = [
    f'Key stats for : {country}', html.Br(),
    f'The most popular Major Category by sales volume was: {top_major_cat}', html.Br(),
    f'The highest sales value month was: {top_sales_month}'
    ]
    return stats_list

if __name__ == '__main__':
    app.run_server(debug=True)