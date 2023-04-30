import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import plotly.graph_objs as go
from neo4j import GraphDatabase
from neo4j_utils import getFaculty

from mysql_utils import get_university, get_faculty_counts
from mongodb_utils import getkeywords

neo_db = db = GraphDatabase.driver('bolt://localhost:7687')

app = Dash(__name__)

# Get the data for the keywords table
keywords_data = getkeywords()
keywords = [row['Keyword'] for row in keywords_data]
counts = [row['Count'] for row in keywords_data]

# Create a bar chart trace for the keywords table data
keywords_trace = go.Bar(x=keywords, y=counts, name='Keywords')

# Get the data for the faculty counts bar chart
faculty_counts_data = get_faculty_counts()
universities = [row['name'] for row in faculty_counts_data]
counts = [row['num_faculty'] for row in faculty_counts_data]

# Create a bar chart trace for the faculty counts data
faculty_counts_trace = go.Bar(x=universities, y=counts, name='Faculty Counts')

app.layout = html.Div([
    html.Div(children='UIUC Resarch Collaboration'),
    html.Div([
        html.Div([
            html.H2('UIUC Faculty in Machine Learning'),
            dash_table.DataTable(
                id='faculty-table',
                columns=[{'name': i, 'id': i} for i in ['Faculty Name', 'KRC']],
                data=getFaculty(),
                page_size=10
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '50px'}),
        html.Div([
            html.H2('Top 10 Most Popular Keywords'),
            dash_table.DataTable(
                id='keywords-table',
                columns=[{'name': i, 'id': i} for i in ['Keyword', 'Count']],
                data=keywords_data,
                page_size=10
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ], style={'margin-top': '50px'}),
    html.Div([
        html.H2('Top 10 Universities by Faculty Count in "Data" Keywords'),
        dcc.Graph(
            id='faculty-counts-graph',
            figure={
                'data': [faculty_counts_trace],
                'layout': {
                    'title': 'Top 10 Universities by Faculty Count in "Data" Keywords'
                }
            }
        )
    ], style={'margin-top': '50px'}),
])

if __name__ == '__main__':
    app.run_server()
