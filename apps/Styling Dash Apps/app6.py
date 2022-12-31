import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
logo_link = '../../data/external/e_com_logo.png'
# logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'

ecom_category = ecom_sales.groupby(['Major Category','Minor Category']).size().reset_index(name='Total Orders').sort_values(by='Total Orders', ascending=False).reset_index(drop=True)

top_cat = ecom_category.loc[0]['Minor Category']
ecom_bar = px.bar(ecom_category, x='Total Orders', y='Minor Category', color='Major Category')

# Set the font color of the bar chart
ecom_bar.update_layout({'yaxis':{'dtick':1, 'categoryorder':'total ascending'}, 'paper_bgcolor':'black', 'font': {'color':'white'}})

app = dash.Dash(__name__)

app.layout = html.Div([
    # Set the new white-text image
    html.Img(src=app.get_asset_url("e_com_logo.png"),
    #src=logo_link,
    style={'width':'165px', 'height':'50px'}),
    html.H1('Top Sales Categories'),
    html.Div(dcc.Graph(figure=ecom_bar,style={'width':'500px', 'height':'350px', 'margin':'auto'})),
    html.Br(),
    html.Span(children=[
    'The top category was: ',
    html.B(top_cat),
    html.Br(),
    html.I('Copyright E-Com INC')])
    ], style={'text-align':'center', 'font-size':22,
              # Update the background color to the entire app
              'background-color':'black',
              # Change the text color for the whole app
              'color':'white'
               })

if __name__ == '__main__':
    app.run_server(debug=True)