import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "Projet 1.xlsx")

spectre = pd.read_excel(fichier_csv, sheet_name="Obj4", skiprows=1)

x = spectre["Temps (minutes)"].to_numpy()

y1 = spectre["AT"].to_numpy()
y2 = spectre["AC"].to_numpy()
y3 = spectre["MEN"].to_numpy()
y4 = spectre["MN"].to_numpy()

# Supprimer les deux premiers points abberants

y1 = y1[2:]
y2 = y2[2:]
y3 = y3[2:] 
y4 = y4[2:]
x = x[2:]

def nettoyer(x, y):
    masque = np.isfinite(x) & np.isfinite(y)
    return x[masque], y[masque]

def r2(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot

x1, y1 = nettoyer(x, y1)
x2, y2 = nettoyer(x, y2)
x3, y3 = nettoyer(x, y3)
x4, y4 = nettoyer(x, y4)

a = np.mean(y1)
b = np.mean(y2)
c = np.mean(y3)
d = np.mean(y4)

print(f"AT (4)  : I(t) = {a:.4f}  |  R² = {r2(y1, np.full_like(y1, a)):.4f}")
print(f"AC (3)  : I(t) = {b:.4f}  |  R² = {r2(y2, np.full_like(y2, b)):.4f}")
print(f"MEN (2) : I(t) = {c:.4f}  |  R² = {r2(y3, np.full_like(y3, c)):.4f}")
print(f"MN (1)  : I(t) = {d:.4f}  |  R² = {r2(y4, np.full_like(y4, d)):.4f}")

x_fit = np.linspace(np.nanmin(x), np.nanmax(x), 300)

plt.figure(figsize=(10, 6))
plt.plot(x4, y4, label="Lampe 1", linestyle='', marker='d', markersize=4, color="#FFA500")
plt.plot(x3, y3, label="Lampe 2", linestyle='', marker='^', markersize=4, color="#008000")
plt.plot(x2, y2, label="Lampe 3", linestyle='', marker='s', markersize=4, color="#007980")
plt.plot(x1, y1, label="Lampe 4", linestyle='', marker='o', markersize=4, color="#800080")

plt.plot(x_fit, np.full_like(x_fit, a), linestyle='-', color="#800080", alpha=0.6)
plt.plot(x_fit, np.full_like(x_fit, b), linestyle='-', color="#007980", alpha=0.6)
plt.plot(x_fit, np.full_like(x_fit, c), linestyle='-', color="#008000", alpha=0.6)
plt.plot(x_fit, np.full_like(x_fit, d), linestyle='-', color="#FFA500", alpha=0.6)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel("Temps (minutes)", fontsize=20)
plt.ylabel("Intensité (lux)", fontsize=20)
plt.legend(fontsize=20)
#plt.savefig("intensite_x_temps.png", bbox_inches='tight', dpi=600)
plt.show()