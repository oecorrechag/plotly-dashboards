import dash
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('../../data/raw/ecom_sales.csv')
ecom_sales = ecom_sales.groupby(['Year-Month','Country'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')

line_fig = px.line(data_frame=ecom_sales, x='Year-Month', y='Total Sales ($)', title='Total Sales by Month', color='Country')

# Create the Dash app
app = dash.Dash(__name__)

# Set up the layout with a single graph
app.layout = dcc.Graph(id='my-line-graph',
  # Insert the line graph
  figure=line_fig)

# Set the app to run in development mode
if __name__ == '__main__':
    app.run_server(debug=True)