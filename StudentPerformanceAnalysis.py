import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import math

root = Tk()
root.title("Student Performance Analysis")
root.geometry("600x250")

root.grid_rowconfigure(index=0, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)

filepath = ""  # path
df_mat = None  # DataFrame 
spalt = []

# Datei öfnen
def open_file():
    global filepath, df_mat, spalt
    filepath = filedialog.askopenfilename(title="Choose a file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if filepath:  
        print(f"File selected: {filepath}")
        df_mat = pd.read_csv(filepath, sep=None, engine='python')  
        df_mat["anwesenheit"] = 93 - df_mat['absences']  # neuen spalte erstellen
        spalt = df_mat.columns.tolist()
        
        
        

        # select
        column_selector["state"] = "readonly"
        calculate_button["state"] = "normal"
        calculate_button1["state"] = "normal"
        gruppen['values'] = spalt
        
# statistic calculation
def calculate_stats():
    if df_mat is None:
        print("wählen zuerst ein Datei aus")
        return

    selected_colum = column_selector.get()  # Spalte (G1, G2, G3)

    if selected_colum not in ["first period", "second period", "final"]:
        print("wählen  eine bestimte Spalte aus")
        return

    print(f"Spalte: {selected_colum}")
    if selected_colum == "first period":
        selected_column = "G1"
    elif selected_colum == "second period":
        selected_column = "G2"
    else:
        selected_column = "G3"
    # Korrelationskoeffizient
    koef_cor = df_mat[selected_column].corr(df_mat["anwesenheit"])
    print(f"Korrelationskoeffizient ({selected_column} и Anwesenheit): {koef_cor:.4f}")

    # H-statistik
    anova_results = {}
    for cat_col in df_mat.columns[:-5]:  # onhe letzten 4 spalten
        groups = [df_mat[df_mat[cat_col] == cat][selected_column] for cat in df_mat[cat_col].unique()]
        f_stat, p_valu = stats.kruskal(*groups)
        p_value = math.e**(-p_valu)
        if enabled.get() == 1: # analöse nur kriterienswerte
            if p_value >= 0.95:
                anova_results[cat_col] = {'H-statistic': f_stat, 'p-value': p_value}
        else:
            anova_results[cat_col] = {'H-statistic': f_stat, 'p-value': p_value}
        

    anova_df = pd.DataFrame(anova_results).T
    print(anova_df.applymap(lambda x: f'{x:.8f}'))

    # Grafik
    plt.figure(figsize=(10, 8))
    sns.barplot(x=anova_df.index, y=anova_df['p-value'], palette="coolwarm")

    plt.axhline(y=math.e**(-0.05), color='red', linestyle='--', label="Kritische Stufe (0.95)")

    for i, p in enumerate(anova_df['p-value']):
        plt.text(i, p + 0.01, f"{p:.2f}", ha='center', fontsize=10, color='black')

    plt.xticks(rotation=90)
    plt.ylim(0, max(anova_df['p-value']) + 0.05)
    plt.ylabel('p-value')
    plt.xlabel('Parametr')
    plt.title(f'H-statistic: exp(-p) ({selected_column})')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.show()



def calculate_grup():
    if df_mat is None:
        print("wählen zuerst ein Datei aus")
        return

    selected_colum = column_selector.get()  # Spalte (G1, G2, G3)

    if selected_colum not in ["first period", "second period", "final"]:
        print("wählen  eine bestimte Spalte aus")
        return
    gruppens = gruppen.get() #Groupenauswahl
    if gruppens not in spalt:
        print("wählen  eine bestimte Grupe aus")
        return
    

    print(f"Spalte: {selected_colum}")
    if selected_colum == "first period":
        selected_column = "G1"
    elif selected_colum == "second period":
        selected_column = "G2"
    else:
        selected_column = "G3"
    
    # Berechnung von Mittelwert, Median und Standardabweichung der Noten
   
    
   
    mean_values = df_mat.groupby(gruppens)[selected_column].mean()
    median_values = df_mat.groupby(gruppens)[selected_column].median()
    stabw_values = df_mat.groupby(gruppens)[selected_column].std()
    print(mean_values)
    print(median_values)
    print(stabw_values)
   

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Grafik der Durchschnittswerte
    sns.barplot(x=mean_values.index, y=mean_values.values, ax=axes[0], palette="Blues")
    axes[0].set_title("Durchschnittswerte")
    axes[0].set_ylabel("Mean")

    # Grafik der Medianwerte
    sns.barplot(x=median_values.index, y=median_values.values, ax=axes[1], palette="Greens")
    axes[1].set_title("Medianwerte")
    axes[1].set_ylabel("Median")

    # Darstellung der Standardabweichung
    sns.barplot(x=stabw_values.index, y=stabw_values.values, ax=axes[2], palette="Reds")
    axes[2].set_title("Standardabweichung")
    axes[2].set_ylabel("Std Deviation")

    # grafikeinstellungen
    for ax in axes:
        ax.set_xlabel("Groupen")
        ax.set_ylim(0, max(mean_values.max(), median_values.max(), stabw_values.max()) * 1.2)
        ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()


# öffnen taste
open_button = ttk.Button(root, text="Datei öfnen", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10, pady=5)

# selektor
column_selector = ttk.Combobox(root, values=["first period", "second period", "final"], state="disabled")
column_selector.grid(column=0, row=2, sticky=NSEW, padx=10, pady=5)
column_selector.set("wählen eine Spalte aus")

# kalkulation taste
calculate_button = ttk.Button(root, text="Kalkulieren", command=calculate_stats, state="disabled")
calculate_button.grid(column=0, row=3, sticky=NSEW, padx=10, pady=5)

#  Checkbutton für nur kriterienswerte
enabled = IntVar()
kriteriumswerte1 = ttk.Checkbutton(text="Nur Kriteriumswerte", variable=enabled)
kriteriumswerte1.grid(column=0, row=4, sticky=NSEW, padx=10, pady=5)
gruppen = ttk.Combobox(values=spalt)
gruppen.grid(column=0, row=5, sticky=NSEW, padx=10, pady=5)
gruppen.set("wählen eine Grupe aus")
calculate_button1 = ttk.Button(root, text="Kalkulieren", command=calculate_grup, state="disabled")
calculate_button1.grid(column=0, row=6, sticky=NSEW, padx=10, pady=5)

root.mainloop()
