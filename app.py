import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State, dash_table

from neo4j import GraphDatabase

from mysql_utils import get_university
from neo4j_utils import getFaculty
from mongodb_utils import getkeywords


neo_db = db = GraphDatabase.driver('bolt://localhost:7687')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='My First App with Data'),
    html.Div([
        dash_table.DataTable(
            id='keywords-table',
            columns=[{'name': i, 'id': i} for i in ['Keyword', 'Count']],
            data=getkeywords(),
            page_size=10
        ),
        dash_table.DataTable(
            id='faculty-table',
            columns=[{'name': i, 'id': i} for i in ['Faculty Name', 'KRC']],
            data=getFaculty(),
            page_size=10
        )
    ], style={'display': 'flex'}),
])

if __name__ == '__main__':
    app.run_server()


