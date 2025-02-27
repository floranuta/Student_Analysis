import pandas as pd
df0 = pd.read_csv("student-mat.csv", delimiter=";")
def fehler_suche(df1):
    #  Dateien einlesen mit korrektem Trennzeichen
    df1 = pd.read_csv("student-mat.csv", delimiter=";")
    

    # Entfernt zusätzliche Leerzeichen um Spaltennamen
    df1.columns = df1.columns.str.strip()  
   

    # Überprüfen der Spaltennamen
    print("Spalten in df1:", df1.columns)
    


    # Überprüfen auf fehlende Werte (Null-Werte) in allen Spalten
    null_values1 = df1.isnull().sum()  
    

    # Zeigt die Spalten mit Null-Werten an
    print("Null-Werte in den Spalten:\n", null_values1)
    

    # Wenn nötig, nur die Spalten mit Null-Werten anzeigen
    print("\nSpalten mit Null-Werten:")
    print(null_values1[null_values1 > 0])
   



    # 1. Überprüfung auf ungültige Werte in den Noten (sollte zwischen 0 und 20 sein)
    for column in ['G1', 'G2', 'G3']:
        df1.loc[(df1[column] > 20) | (df1[column] < 0), column] = df1[column].mean()  # Fehlerhafte Noten auf den Mittelwert setzen
        
    # 2. Überprüfung auf ungültige Werte im Alter (sollte zwischen 0 und 100 sein)
    df1.loc[(df1['age'] > 100) | (df1['age'] < 0), 'age'] = df1['age'].mean()
    
    # 3. Überprüfung auf gültige Werte im Geschlecht (sollte nur 'M' oder 'F' sein)
    df1['sex'] = df1['sex'].apply(lambda x: x if x in ['M', 'F'] else 'M')
    

    # 4. Überprüfung auf eindeutige Werte in den Spalten
    print("Einzigartige Werte in df1:")
    for col in df1.columns:
        print(f"{col}: {df1[col].unique()}")

   
    # 5. Überprüfung auf Ausreißer (z.B. Absence > 100 oder studytime > 5)
    df1.loc[df1['absences'] > 100, 'absences'] = df1['absences'].mean()
    
    df1.loc[df1['studytime'] > 5, 'studytime'] = df1['studytime'].mean()
    

    # Speichern der korrigierten Daten
    df1.to_csv("student-mat_korrekt.csv", index=False)
    

    print("\nCode ist ohne Fehler")
df5 = fehler_suche(df0)

