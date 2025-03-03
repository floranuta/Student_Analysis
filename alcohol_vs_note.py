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

# 4. Берем среднее потребление алкоголя (Dalc - будни, Walc - выходные)
df["Alkohol_Konsum"] = (df["Dalc"] + df["Walc"]) / 2  # Среднее потребление алкоголя

# 5. Группируем данные по уровню потребления алкоголя и предмету
df_grouped = df.groupby(["Alkohol_Konsum", "Fach"], as_index=False).mean(numeric_only=True)

# 6. Строим график зависимости оценок (G3) от потребления алкоголя
fig_bar = px.bar(
    df_grouped,
    x="Alkohol_Konsum",
    y="G3",  # Используем оригинальный столбец
    color="Fach",
    barmode="group",
    title="Durchschnittliche Note nach Alkoholkonsum",
    labels={"G3": "Note", "Alkohol_Konsum": "Alkoholkonsum (Skala 1-5)"}
)

# 7. Dash-интерфейс
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Analyse der Studentenleistungen", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(figure=fig_bar, config={'staticPlot': True})  # Гистограмма
    ], style={"width": "80%", "margin": "auto"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
