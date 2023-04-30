from dash import Dash, html, dash_table
import pandas as pd
import pymysql

print('running')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='My First App with Data')
])

if __name__ == '__main__':
    mysqlconnect()
    app.run_server(debug=True)