import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output


d1 = pd.read_csv("student-mat.csv", sep=";")
null_cols = d1.isnull().sum()
null_cols = null_cols[null_cols > 0]  

if not null_cols.empty:
    print("Die Spalten mit dem NULL Wertenin Mathe:")
    print(null_cols)
else:
    print("Keine Null werten in dem Mathe DataFrame.")

print("Überprüfen die numerischen Spalten in dem Mathe DataFrame....")

list_numeric_columns = d1.select_dtypes(include=['int64', 'float64']).columns
for col in list_numeric_columns:
    if pd.to_numeric(d1[col], errors='coerce').notnull().all():
       pass
    else:
        print("Die Spalte", col, "hat nicht numerische Werten.")

print("Überprüfen die String Spalten in dem Mathe DataFrame...")

string_columns = d1.select_dtypes(include=['object'])
empty_strings = (string_columns.apply(lambda col: col.str.strip() == "").any())

if empty_strings.any():
    print("Diese Spalten haben leer Werten:", empty_strings[empty_strings].index.tolist())

d2 = pd.read_csv("student-por.csv", sep=";")
null_cols = d2.isnull().sum()
null_cols = null_cols[null_cols > 0]
if not null_cols.empty:
    print("Die Spalten mit dem NULL Wertenin Portugiesisch:")
    print(null_cols)
else:
    print("Keine Null werten in dem Portugaise DataFrame.")

print("Überprüfen die numerischen Spalten in dem Portugiesisch DataFrame....")

list_numeric_columns = d2.select_dtypes(include=['int64', 'float64']).columns
for col in list_numeric_columns:
    if pd.to_numeric(d2[col], errors='coerce').notnull().all():
       pass
    else:
        print("Die Spalte", col, "hat nicht numerische Werten.")

print("Überprüfen die String Spalten in dem Portugiesisch DataFrame...")

string_columns = d2.select_dtypes(include=['object'])
empty_strings = (string_columns.apply(lambda col: col.str.strip() == "").any())

if empty_strings.any():
    print("Diese Spalten haben leer Werten:", empty_strings[empty_strings].index.tolist())


