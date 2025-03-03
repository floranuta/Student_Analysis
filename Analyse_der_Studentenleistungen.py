import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# 1. Daten laden (Загрузка данных)
df_math = pd.read_csv("student-mat.csv", delimiter=";")
df_por = pd.read_csv("student-por.csv", delimiter=";")

# 2. Eine neue Spalte "Fach" hinzufügen, um das Fach zu unterscheiden (Добавляем колонку "Fach" для обозначения предмета)
df_math["Fach"] = "Mathematik"
df_por["Fach"] = "Portugiesisch"

# 3. Beide DataFrames zusammenfügen (Объединяем два датафрейма в один)
df = pd.concat([df_math, df_por])

# 4. Kolonne "G3" umbenennen zu "Note" (Переименовываем "G3" в "Note")
df.rename(columns={"G3": "Note"}, inplace=True)

# 5. Erstellen eines Kreisdiagramms (Круговая диаграмма по полу)
fig_pie = px.pie(df, names="sex", title="Verteilung der Studenten nach Geschlecht")

# 6. Histogramm: Notenverteilung nach Geschlecht und Fach (Гистограмма успеваемости по полу и предмету)
fig_hist = px.histogram(df, x="Note", color="sex", facet_col="Fach",
                        title="Leistungsanalyse nach Geschlecht und Fach", barmode="overlay")

# 7. Подписываем оси для лучшего понимания
fig_hist.update_layout(
    xaxis_title="Note",  # Итоговая оценка
    yaxis_title="Anzahl der Schüler",  # Количество учеников
    title_x=0.55  # Смещаем заголовок гистограмм в центр
)

# 8. Dash-Anwendung (Создание интерфейса Dash)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Analyse der Studentenleistungen", style={'textAlign': 'center'}),  # Центрируем заголовок
    
    html.Div(style={'display': 'flex', 'align-items': 'center'}, children=[
        html.Div(dcc.Graph(figure=fig_pie), style={'width': '35%', 'margin-right': '5%'}),  # Круговая диаграмма, немного левее
        html.Div(dcc.Graph(figure=fig_hist), style={'width': '60%'})  # Гистограмма
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
