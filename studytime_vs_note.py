import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# 1. Загрузка данных
df_math = pd.read_csv("student-mat.csv", delimiter=";")
df_por = pd.read_csv("student-por.csv", delimiter=";")

# 2. Добавляем колонку "Fach" для обозначения предмета
df_math["Fach"] = "Mathematik"
df_por["Fach"] = "Portugiesisch"

# 3. Объединяем два датафрейма в один
df = pd.concat([df_math, df_por])

# 4. Преобразуем столбец studytime в категорию (если он вдруг строковый)
df["studytime"] = pd.to_numeric(df["studytime"], errors="coerce")

# 5. Строим график зависимости оценок (G3) от времени на учебу (studytime)
df_grouped = df.groupby(["studytime", "Fach"], as_index=False).mean(numeric_only=True)  # Берем только числовые столбцы

fig_line = px.line(
    df_grouped,
    x="studytime",
    y="G3",  # Используем оригинальный столбец
    color="Fach",
    title="Durchschnittliche Note nach Studienzeit",
    labels={"G3": "Note", "studytime": "Studienzeit (Stunden pro Woche)"}  # Подписываем оси
)

# 6. Dash-интерфейс
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Analyse der Studentenleistungen", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(figure=fig_line, config={'displayModeBar': False})  # Линейный график
    ], style={"width": "80%", "margin": "auto"})
])

if __name__ == '__main__':
    app.run_server(debug=True)

