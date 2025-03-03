import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import scipy.stats as stats

# 1. Laden der Daten aus CSV-Dateien
math_df = pd.read_csv("student-mat.csv", sep=";")
por_df = pd.read_csv("student-por.csv", sep=";")

# 2. Berechnung der Korrelation zwischen Fehlzeiten und Noten (G1, G2, G3)
def correlation_analysis(df, subject):
    print(f"Korrelation in {subject}:")
    print(df[['absences', 'G1', 'G2', 'G3']].corr())
    print("-" * 40)

correlation_analysis(math_df, "Mathematik")
correlation_analysis(por_df, "Portugiesisch")

# 3. Visualisierung der Korrelationen mit einer Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(math_df[['absences', 'G1', 'G2', 'G3']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Korrelationsmatrix Mathematik")
plt.show()

# 4. Lineare Regression zur Untersuchung des Zusammenhangs zwischen Fehlzeiten und G3
sns.lmplot(x='absences', y='G3', data=math_df, aspect=1.5, line_kws={'color': 'red'})
plt.title("Regression: Anwesenheit vs. G3 in Mathematik")
plt.show()

# 5. Statistischer Test (Spearman-Korrelation) zur Überprüfung der Signifikanz
def spearman_test(df, subject):
    rho, p_value = stats.spearmanr(df['absences'], df['G3'])
    print(f"Spearman-Korrelation in {subject}: rho={rho:.2f}, p-Wert={p_value:.4f}")
    print("-" * 40)

spearman_test(math_df, "Mathematik")
spearman_test(por_df, "Portugiesisch")
