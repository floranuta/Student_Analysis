import pandas as pd

# Laden der Daten
df_math = pd.read_csv("student-mat.csv", sep=";")
df_por = pd.read_csv("student-por.csv", sep=";")

# Zusammenführen der beiden Datensätze
merge_columns = ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet"]
df = pd.merge(df_math, df_por, on=merge_columns, suffixes=('_math', '_por'))

# Gruppierung nach Geschlecht
grouped_by_gender = df.groupby("sex")[["G3_math", "G3_por"]].mean()
print("Durchschnittliche Noten nach Geschlecht:\n", grouped_by_gender)

import pandas as pd

df = pd.read_csv("student-mat.csv", sep=";")

# Berechnung von Mittelwert, Median und Standardabweichung der Noten
stats = df[["G3"]].agg(["mean", "median", "std"])
print("Deskriptive Statistik der Noten:\n", stats)
