# Importieren der notwendigen Bibliotheken
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Laden der Datensätze
df_math = pd.read_csv("student-mat.csv", sep=";")
df_por = pd.read_csv("student-por.csv", sep=";")

# Zusammenführen der Datensätze basierend auf gemeinsamen Spalten
merge_columns = ["school", "sex", "age", "address", "famsize", "Pstatus",
                 "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet"]
df = pd.merge(df_math, df_por, on=merge_columns, suffixes=('_math', '_por'))

# 1. Gruppierung nach Geschlecht und Berechnung der Durchschnittsnoten
grouped_by_gender = df.groupby("sex")[["G3_math", "G3_por"]].mean()
print("Durchschnittliche Noten nach Geschlecht:\n", grouped_by_gender)

# 2. Berechnung von Mittelwert, Median und Standardabweichung der Noten (Mathematik)
stats_math = df_math["G3"].agg(["mean", "median", "std"])
print("\nDeskriptive Statistik der Mathematiknoten:\n", stats_math)

# 3. Untersuchung der Korrelation zwischen Abwesenheiten und Noten
sns.scatterplot(x=df_math["absences"], y=df_math["G3"])
plt.xlabel("Anzahl der Abwesenheiten")
plt.ylabel("Endnote")
plt.title("Korrelation zwischen Abwesenheiten und Noten")
plt.show()

# Berechnung des Korrelationskoeffizienten
correlation = df_math["absences"].corr(df_math["G3"])
print("\nKorrelationskoeffizient zwischen Abwesenheiten und Endnote:", correlation)

# 4. Vergleich der Noten zwischen zwei Schulen (GP und MS)
gp_grades = df_math[df_math["school"] == "GP"]["G3"]
ms_grades = df_math[df_math["school"] == "MS"]["G3"]

print("\nDurchschnittliche Noten pro Schule:")
print("GP - Mittelwert: {:.2f}, Standardabweichung: {:.2f}".format(gp_grades.mean(), gp_grades.std()))
print("MS - Mittelwert: {:.2f}, Standardabweichung: {:.2f}".format(ms_grades.mean(), ms_grades.std()))

# Durchführung eines unabhängigen t-Tests
t_stat, p_value = stats.ttest_ind(gp_grades, ms_grades)
print("t-Test zwischen Schulen: t-Statistik = {:.2f}, p-Wert = {:.4f}".format(t_stat, p_value))

# 5. Vergleich der Noten nach Altersgruppen mit ANOVA
anova_result = stats.f_oneway(*(df_math[df_math['age'] == age]['G3'] for age in df_math['age'].unique()))
print("\nANOVA-Ergebnis für Altersgruppen: F-Statistik = {:.2f}, p-Wert = {:.4f}".format(anova_result.statistic, anova_result.pvalue))

# 6. Vergleich der Noten nach Geschlecht
male_grades = df_math[df_math["sex"] == "M"]["G3"]
female_grades = df_math[df_math["sex"] == "F"]["G3"]

print("\nDurchschnittliche Noten nach Geschlecht:")
print("Männer - Mittelwert: {:.2f}, Standardabweichung: {:.2f}".format(male_grades.mean(), male_grades.std()))
print("Frauen - Mittelwert: {:.2f}, Standardabweichung: {:.2f}".format(female_grades.mean(), female_grades.std()))

# Durchführung eines unabhängigen t-Tests für Geschlecht
t_stat, p_value = stats.ttest_ind(male_grades, female_grades)
print("t-Test zwischen Geschlechtern: t-Statistik = {:.2f}, p-Wert = {:.4f}".format(t_stat, p_value))
