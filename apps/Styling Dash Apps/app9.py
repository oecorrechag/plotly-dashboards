import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
logo_link = '../../data/external/e_com_logo.png'
# logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'

ecom_line = ecom_sales.groupby('Year-Month')['OrderValue'].agg('sum').reset_index(name='TotalSales')

line_fig = px.line(data_frame=ecom_line, x='Year-Month', y='TotalSales',title='Total Sales by Month')
line_fig.update_layout({'paper_bgcolor':'rgb(224, 255, 252)' }) 

ecom_bar = ecom_sales.groupby('Country')['OrderValue'].agg('sum').reset_index(name='TotalSales')

bar_fig = px.bar(data_frame=ecom_bar, x='TotalSales', y='Country', orientation='h',title='Total Sales by Country')
bar_fig.update_layout({'yaxis':{'dtick':1, 'categoryorder':'total ascending'}, 'paper_bgcolor':'rgb(224, 255, 252)'})


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
      html.Img(src=app.get_asset_url("e_com_logo.png"),
               # Place the logo side-by-side the H1 with required margin
               style={'display':'inline-block', 'margin':'25px'}),
      html.H1(children=['Sales Figures'],
              # Make the H1 side-by-side with the logos
              style={'display':'inline-block'}), 
      html.Img(src=app.get_asset_url("e_com_logo.png"),
               # Place the logo side-by-side the H1 with required margin
               style={'display':'inline-block', 'margin':'25px'})]),
    html.Div(
        dcc.Graph(figure=line_fig), 
        # Ensure graphs are correct size, side-by-side with required margin
        style={'width':'500px', 'display':'inline-block', 'margin':'5px'}), 
    html.Div(
      	dcc.Graph(figure=bar_fig),
        # Ensure graphs are correct size, side-by-side with required margin
    	style={'width':'350px', 'display':'inline-block', 'margin':'5px'}), 
    html.H3(f'The largest order quantity was {ecom_sales.Quantity.max()}')
    ],style={'text-align':'center', 'font-size':22, 'background-color':'rgb(224, 255, 252)'})

if __name__ == '__main__':
    app.run_server(debug=True)