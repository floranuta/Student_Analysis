import pandas as pd

# Zwei Dateien einlesen mit korrektem Trennzeichen
df1 = pd.read_csv("student-mat.csv", delimiter=";")
df2 = pd.read_csv("student-por.csv", delimiter=";")

# Entfernt zusätzliche Leerzeichen um Spaltennamen
df1.columns = df1.columns.str.strip()  
df2.columns = df2.columns.str.strip()

# Überprüfen der Spaltennamen
print("Spalten in df1:", df1.columns)
print("Spalten in df2:", df2.columns)


# Überprüfen auf fehlende Werte (Null-Werte) in allen Spalten
null_values1 = df1.isnull().sum()  
null_values2 = df2.isnull().sum()

# Zeigt die Spalten mit Null-Werten an
print("Null-Werte in den Spalten:\n", null_values1)
print("Null-Werte in den Spalten:\n", null_values2)

# Wenn nötig, nur die Spalten mit Null-Werten anzeigen
print("\nSpalten mit Null-Werten:")
print(null_values1[null_values1 > 0])
print(null_values2[null_values2 > 0])



# 1. Überprüfung auf ungültige Werte in den Noten (sollte zwischen 0 und 20 sein)
for column in ['G1', 'G2', 'G3']:
    df1.loc[(df1[column] > 20) | (df1[column] < 0), column] = df1[column].mean()  # Fehlerhafte Noten auf den Mittelwert setzen
    df2.loc[(df2[column] > 20) | (df2[column] < 0), column] = df2[column].mean()

# 2. Überprüfung auf ungültige Werte im Alter (sollte zwischen 0 und 100 sein)
df1.loc[(df1['age'] > 100) | (df1['age'] < 0), 'age'] = df1['age'].mean()
df2.loc[(df2['age'] > 100) | (df2['age'] < 0), 'age'] = df2['age'].mean()

# 3. Überprüfung auf gültige Werte im Geschlecht (sollte nur 'M' oder 'F' sein)
df1['sex'] = df1['sex'].apply(lambda x: x if x in ['M', 'F'] else 'M')
df2['sex'] = df2['sex'].apply(lambda x: x if x in ['M', 'F'] else 'M')

# 4. Überprüfung auf eindeutige Werte in den Spalten
print("Einzigartige Werte in df1:")
for col in df1.columns:
    print(f"{col}: {df1[col].unique()}")

print("\nEinzigartige Werte in df2:")
for col in df2.columns:
    print(f"{col}: {df2[col].unique()}")

# 5. Überprüfung auf Ausreißer (z.B. Absence > 100 oder studytime > 5)
df1.loc[df1['absences'] > 100, 'absences'] = df1['absences'].mean()
df2.loc[df2['absences'] > 100, 'absences'] = df2['absences'].mean()

df1.loc[df1['studytime'] > 5, 'studytime'] = df1['studytime'].mean()
df2.loc[df2['studytime'] > 5, 'studytime'] = df2['studytime'].mean()

# Speichern der korrigierten Daten
df1.to_csv("student-mat_korrekt.csv", index=False)
df2.to_csv("student-por_korrekt.csv", index=False)

print("\nCode ist ohne Fehler")


