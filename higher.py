import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html

# 1. Daten laden
df_math = pd.read_csv("student-mat.csv", delimiter=";")
df_por = pd.read_csv("student-por.csv", delimiter=";")

# 2. Datensätze kombinieren
df = pd.concat([df_math, df_por])

# 3. Durchschnittsnoten berechnen
mean_yes = df[df["higher"] == "yes"]["G3"].mean()
mean_no = df[df["higher"] == "no"]["G3"].mean()

# 4. Funktion zur Erstellung von Halbkreisdiagrammen
def create_gauge_chart(value, title, color):
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={
                "shape": "angular",
                "bar": {"color": color},
                "axis": {"range": [0, 20]},
                "steps": [
                    {"range": [0, value], "color": color}  # Bereich bis zum Wert ausfüllen
                ]
            },
            number={"font": {"size": 48}},
        )
    ).update_layout(
        title={"text": title, "x": 0.5},
        height=350,
        width=450,
        margin=dict(l=20, r=20, t=50, b=20),
    )

# 5. Diagramme erstellen
fig_yes = create_gauge_chart(mean_yes, "Will studieren", "blue")
fig_no = create_gauge_chart(mean_no, "Will nicht studieren", "red")

# 6. Dash App erstellen
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Analyse der Studentenleistungen", style={"textAlign": "center"}),
    html.H3("Durchschnittsnote", style={"textAlign": "center"}),
    html.Div([
        html.Div(dcc.Graph(figure=fig_yes, config={'displayModeBar': False}), style={"display": "inline-block", "padding": "20px"}),
        html.Div(dcc.Graph(figure=fig_no, config={'displayModeBar': False}), style={"display": "inline-block", "padding": "20px"}),
    ], style={"textAlign": "center", "overflow": "hidden"})  # Scrollen verhindern
])

if __name__ == '__main__':
    app.run_server(debug=True)
