import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy.optimize import curve_fit

#lampe 1 : MN
#lampe 2 : MEN
#lampe 3 : AC
#lampe 4 : AT

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "Projet 1.xlsx")

spectre = pd.read_excel(fichier_csv, sheet_name="Obj2", skiprows=1)

# Conversion en mètres pour que a / x**2 soit dans des ordres de grandeur cohérents
x = spectre["Distance (cm)"].to_numpy() / 100

y1 = spectre["AT"].to_numpy()
y2 = spectre["AC"].to_numpy()
y3 = spectre["MEN"].to_numpy()
y4 = spectre["MN"].to_numpy()

# Exclure le premier point x=0 (division par zéro dans le modèle)
masque = x > 0
x = x[masque]
y1 = y1[masque]
y2 = y2[masque]
y3 = y3[masque]
y4 = y4[masque]

def modele(x, a):
    return a / x**2

def p0_initial(x, y):
    a0 = y[0] * x[0]**2
    return [a0]

def r2(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot

x_fit = np.linspace(x.min(), x.max(), 300)

params1, _ = curve_fit(modele, x, y1, p0=p0_initial(x, y1), maxfev=5000)
params2, _ = curve_fit(modele, x, y2, p0=p0_initial(x, y2), maxfev=5000)
params3, _ = curve_fit(modele, x, y3, p0=p0_initial(x, y3), maxfev=5000)
params4, _ = curve_fit(modele, x, y4, p0=p0_initial(x, y4), maxfev=5000)

y1_fit = modele(x_fit, *params1)
y2_fit = modele(x_fit, *params2)
y3_fit = modele(x_fit, *params3)
y4_fit = modele(x_fit, *params4)

print(f"AT  (4) : I(x) = {params1[0]:.4f} / x²  |  R² = {r2(y1, modele(x, *params1)):.4f}")
print(f"AC  (3) : I(x) = {params2[0]:.4f} / x²  |  R² = {r2(y2, modele(x, *params2)):.4f}")
print(f"MEN (2) : I(x) = {params3[0]:.4f} / x²  |  R² = {r2(y3, modele(x, *params3)):.4f}")
print(f"MN  (1) : I(x) = {params4[0]:.4f} / x²  |  R² = {r2(y4, modele(x, *params4)):.4f}")

plt.figure(figsize=(10, 6))
plt.plot(x * 100, y4, label="Lampe 1", linestyle='', marker='d', markersize=4, color="#FFA500")
plt.plot(x * 100, y3, label="Lampe 2", linestyle='', marker='^', markersize=4, color="#008000")
plt.plot(x * 100, y2, label="Lampe 3", linestyle='', marker='s', markersize=4, color="#007980")
plt.plot(x * 100, y1, label="Lampe 4", linestyle='', marker='o', markersize=4, color="#800080")

plt.plot(x_fit * 100, y1_fit, linestyle='-', color="#800080", alpha=0.6, label="Lampe 4")
plt.plot(x_fit * 100, y2_fit, linestyle='-', color="#007980", alpha=0.6, label="Lampe 3")
plt.plot(x_fit * 100, y3_fit, linestyle='-', color="#008000", alpha=0.6, label="Lampe 2")
plt.plot(x_fit * 100, y4_fit, linestyle='-', color="#FFA500", alpha=0.6, label="Lampe 1")

plt.xlabel("Distance (cm)", fontsize=20)
plt.ylabel("Intensité (lux)", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
#plt.savefig("intensite_x_distance.png", bbox_inches='tight', dpi=600)
plt.show()