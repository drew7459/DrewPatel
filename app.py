import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import plotly.graph_objs as go
from neo4j import GraphDatabase
from neo4j_utils import getFaculty

from mysql_utils import get_university, get_faculty_counts, get_topFaculty, get_faculty_publications, get_favorites, add_favorite, delete_favorite
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
faculty_counts_data = get_faculty_counts("machine learning")
universities = [row['name'] for row in faculty_counts_data]
counts = [row['num_faculty'] for row in faculty_counts_data]

# Create a bar chart trace for the faculty counts data
faculty_counts_trace = go.Bar(x=universities, y=counts, name='Faculty Counts')

# Get the data for the top faculty table
top_faculty_data = get_topFaculty()
top_faculty_data = [{'Faculty Name': row['name'].title(), 'KRC': row['KRC']} for row in top_faculty_data]

favorite_data = get_favorites()
favorite_data = [{'Name': row['name'].title(), 'Email': row['email']} for row in favorite_data]

def create_delete_button_column():
    return {'name': '', 'id': 'delete-button-column', 'presentation': 'markdown',
            'compute': lambda row: f'[{row["id"]}]({row["id"]})'}

app.layout = html.Div([
    html.H1('Research Collaboration', style={'fontSize': 36, 'color': 'red'}),
    html.Div([
        html.Div([
            html.H2('Top Most Popular Keywords'),
            dash_table.DataTable(
                id='keywords-table',
                columns=[{'name': i, 'id': i} for i in ['Keyword', 'Count']],
                data=keywords_data,filter_action='native',
                filter_query='',
                page_size=9
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            html.H2('UIUC Faculty in Machine Learning'),
            dash_table.DataTable(
                id='faculty-table',
                columns=[{'name': i, 'id': i} for i in ['Faculty Name', 'KRC']],
                data=getFaculty(),
                page_size=10
            )
        ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '50px'}),
    ], style={'margin-top': '50px', 'display': 'flex', 'flex-wrap': 'wrap'}),
    html.Div([
        html.H2('Top 10 Universities by Faculty Count by Keyword'),
        html.Div([
            dcc.Input(id='keywords-input', type='text', placeholder='Enter keywords'),
            html.Button('Submit', id='keywords-submit'),
        ]),
        dcc.Graph(
            id='faculty-counts-graph',
            figure={
                'data': [faculty_counts_trace],
                'layout': {
                    'title': 'Top 10 Universities by Faculty Count in "machine learning" Keywords'
                }
            }
        )
    ], style={'margin-top': '50px'}),
    html.Div([
        html.Div([
            html.H2('Top Faculty in "Data" Keywords'),
            dash_table.DataTable(
                id='top-faculty-table',
                columns=[{'name': i, 'id': i} for i in ['Faculty Name', 'KRC']],
                data=top_faculty_data,
                page_size=10
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            html.H2('Faculty Search'),
            dcc.Input(id='faculty-name-input', type='text', placeholder='Enter faculty name'),
            html.Button('Submit', id='faculty-name-submit'),
            html.Button('Add to Favorites', id='add-favorite-button'),
            html.Div(id='add-favorite-output'),
            dash_table.DataTable(
                id='faculty-publications-table',
                columns=[{'name': i, 'id': i} for i in ['Title', 'Year', 'Citations']],
                page_size=10
            )
        ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '50px'}),
    ], style={'margin-top': '50px', 'display': 'flex', 'flex-wrap': 'wrap'}),
    html.Div([
        html.H2('Favorite Professors'),
        dash_table.DataTable(
            id='favorites-table',
            columns=[{'name': i, 'id': i} for i in ['Name', 'Email']],
            data=favorite_data,
            page_size=10,
            editable=True,
            row_deletable=True,
            style_cell_conditional=[{'if': {'column_id': 'Delete'}, 'textAlign': 'center'}]
        )
    ], style={'margin-top': '50px'}),
])

@app.callback(Output('faculty-publications-table', 'data'),
              [Input('faculty-name-submit', 'n_clicks')],
              [State('faculty-name-input', 'value')])
def update_faculty_publications_table(n_clicks, faculty_name):
    if n_clicks is None:
        return dash.no_update

    data = get_faculty_publications(faculty_name)
    data = [{'Title': row['title'], 'Year': row['year'], 'Citations': row['num_citations']} for row in data]

    return data

@app.callback(
    [Output('add-favorite-output', 'children'),
    Output('favorites-table', 'data')],
    [Input('add-favorite-button', 'n_clicks')],
    [State('faculty-name-input', 'value')]
)
def add_favorite_callback(n_clicks, faculty_name):
    print("test")
    if n_clicks is None:
        n_clicks = 0

    if n_clicks > 0:
        add_favorite(faculty_name)
        favorite_data = get_favorites()
        favorite_data = [{'Name': row['name'].title(), 'Email': row['email']} for row in favorite_data]
        return f"{faculty_name} has been added to favorites.", favorite_data

    return dash.no_update


@app.callback(
    Output('faculty-counts-graph', 'figure'),
    [Input('keywords-submit', 'n_clicks')],
    [State('keywords-input', 'value')])
def update_faculty_counts_graph(n_clicks, keywords):
    if n_clicks is None:
        raise PreventUpdate

    # Use the entered keywords to update the faculty counts graph
    faculty_counts_data = get_faculty_counts(keywords)
    universities = [row['name'] for row in faculty_counts_data]
    counts = [row['num_faculty'] for row in faculty_counts_data]
    faculty_counts_trace = go.Bar(x=universities, y=counts, name='Faculty Counts')

    return {'data': [faculty_counts_trace],
            'layout': {'title': f'Top 10 Universities by Faculty Count in "{keywords}" Keywords'}}

"""
@app.callback(
    Output('favorites-table', 'data'),
    Input('favorites-table', 'data_previous'),
    State('favorites-table', 'data'),
)
def update_database(previous_data, current_data):
    if previous_data is None:
        # Initial page load, do nothing
        return current_data

    previous_names = set(row['Name'] for row in previous_data)
    current_names = set(row['Name'] for row in current_data)

    deleted_names = previous_names - current_names
    if deleted_names:
        for name in deleted_names:
            delete_favorite(name)

    return current_data
"""

if __name__ == '__main__':
    app.run_server()
