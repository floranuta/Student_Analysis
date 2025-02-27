import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
d1 = pd.read_csv("student-mat.csv", sep=";")
d2 = pd.read_csv("student-por.csv", sep=";")  # Assuming d2 is another dataframe

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1("Student Analysis Table"),  # Add table header
    dcc.Dropdown(
        id='fach-filter',
        options=[
            {'label': 'Mathematics', 'value': 'd1'},
            {'label': 'Portuguese', 'value': 'd2'}
        ],
        value='d1',  # Set default value to d1
        placeholder="Wählen Sie ein Fach",
        style={'width': '100%', 'font-weight': 'bold'}  # Set fixed width for the filter and make text bold
    ),
    html.Div(id='filters-container', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '5px', 'justify-content': 'flex-start'}),  # Container for filters with reduced gap and aligned to start
    html.Div(
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in d1.columns],
            data=d1.to_dict('records'),
            filter_action="native",
            fixed_rows={'headers': True},  # Fix the header row
            style_table={'height': '400px', 'overflowY': 'auto'},  # Add style to ensure visibility
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}  # Style the header
        ),
        style={'height': '400px', 'overflowY': 'auto'}  # Ensure the parent div has a height
    )
])

@app.callback(
    dash.Output('filters-container', 'children'),
    dash.Input('fach-filter', 'value')
)
def update_filters(selected_fach):
    if selected_fach == 'd2':
        data = d2
    else:
        data = d1

    filters = [
        dcc.Dropdown(
            id='gender-filter',
            options=[{'label': c, 'value': c} for c in data["sex"].unique()],
            placeholder="Wählen Sie ein Geschlecht",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='paid-filter',
            options=[{'label': c, 'value': c} for c in data["paid"].unique()],
            placeholder="Extra paid classes",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='Medu-filter',
            options=[{'label': c, 'value': c} for c in data["Medu"].unique()],
            placeholder="Mother's education",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='Fedu-filter',
            options=[{'label': c, 'value': c} for c in data["Fedu"].unique()],
            placeholder="Father's education",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='Mjob-filter',
            options=[{'label': c, 'value': c} for c in data["Mjob"].unique()],
            placeholder="Mother's job",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='Fjob-filter',
            options=[{'label': c, 'value': c} for c in data["Fjob"].unique()],
            placeholder="Father's job",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='failures-filter',
            options=[{'label': c, 'value': c} for c in data["failures"].unique()],
            placeholder="Number of failures",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='schoolsup-filter',
            options=[{'label': c, 'value': c} for c in data["schoolsup"].unique()],
            placeholder="Extra educational support",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='higher-filter',
            options=[{'label': c, 'value': c} for c in data["higher"].unique()],
            placeholder="Higher education",
            style={'width': '45%'}  # Increase width for the filter
        ),
        dcc.Dropdown(
            id='goout-filter',
            options=[{'label': c, 'value': c} for c in data["goout"].unique()],
            placeholder="Going out with friends",
            style={'width': '45%'}  # Increase width for the filter
        ),
    ]
    return filters

@app.callback(
    dash.Output('table', 'data'),
    dash.Output('table', 'columns'),
    [dash.Input('fach-filter', 'value'),
     dash.Input('gender-filter', 'value'),
     dash.Input('paid-filter', 'value'),
     dash.Input('Medu-filter', 'value'),
     dash.Input('Fedu-filter', 'value'),
     dash.Input('Mjob-filter', 'value'),
     dash.Input('Fjob-filter', 'value'),
     dash.Input('failures-filter', 'value'),
     dash.Input('schoolsup-filter', 'value'),
     dash.Input('higher-filter', 'value'),
     dash.Input('goout-filter', 'value')],
    prevent_initial_call=True  # Prevent callback from firing initially
)
def update_table(selected_fach, selected_sex, selected_paid, selected_Medu, selected_Fedu, selected_Mjob, selected_Fjob, selected_failures, selected_schoolsup, selected_higher, selected_goout):
    if selected_fach == 'd2':
        data = d2
    else:
        data = d1

    filtered_data = data
    if selected_sex:
        filtered_data = filtered_data[filtered_data["sex"] == selected_sex]
    if selected_paid:
        filtered_data = filtered_data[filtered_data["paid"] == selected_paid]
    if selected_Medu:
        filtered_data = filtered_data[filtered_data["Medu"] == selected_Medu]
    if selected_Fedu:
        filtered_data = filtered_data[filtered_data["Fedu"] == selected_Fedu]
    if selected_Mjob:
        filtered_data = filtered_data[filtered_data["Mjob"] == selected_Mjob]
    if selected_Fjob:
        filtered_data = filtered_data[filtered_data["Fjob"] == selected_Fjob]
    if selected_failures:
        filtered_data = filtered_data[filtered_data["failures"] == selected_failures]
    if selected_schoolsup:
        filtered_data = filtered_data[filtered_data["schoolsup"] == selected_schoolsup]
    if selected_higher:
        filtered_data = filtered_data[filtered_data["higher"] == selected_higher]
    if selected_goout:
        filtered_data = filtered_data[filtered_data["goout"] == selected_goout]
    
    columns = [{'name': col, 'id': col} for col in data.columns]
    return filtered_data.to_dict('records'), columns

if __name__ == '__main__':
    app.run_server(debug=True)
