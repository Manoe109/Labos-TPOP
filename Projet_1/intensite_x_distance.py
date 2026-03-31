import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy.optimize import curve_fit

# Couleurs et styles option C
C1, C2, C3, C4 = "black", "#7293C5", "#B99851", "#3B6D11"
LS1, LS2, LS3, LS4 = '-', '--', ':', '-.'

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_xlsx = os.path.join(dossier_script, "Projet 1.xlsx")

df = pd.read_excel(fichier_xlsx, sheet_name="Obj2", skiprows=1)
x  = df["Distance (cm)"].to_numpy()
y1 = df["MN"].to_numpy()   # Lampe 1
y2 = df["MEN"].to_numpy()  # Lampe 2
y3 = df["AC"].to_numpy()   # Lampe 3
y4 = df["AT"].to_numpy()   # Lampe 4

def incertitude(y):
    err = np.zeros_like(y, dtype=float)
    err[y > 20000]                     = 1000  # plage 200 000 lux
    err[(y > 2000) & (y <= 20000)]     = 100   # plage 20 000 lux
    err[(y > 200)  & (y <= 2000)]      = 10    # plage 2 000 lux
    err[y <= 200]                      = 1     # plage 200 lux
    return err

def modele(x, a, b):
    return a * np.exp(b * x)

def p0_initial(x, y):
    a0 = y[0]
    b0 = (np.log(y[-1]) - np.log(y[0])) / (x[-1] - x[0])
    return [a0, b0]

def r2(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot

donnees = [
    ("Lampe 1", y1, C1, 'd', LS1),
    ("Lampe 2", y2, C2, '^', LS2),
    ("Lampe 3", y3, C3, 's', LS3),
    ("Lampe 4", y4, C4, 'o', LS4),
]

x_fit = np.linspace(0, 60, 300)
params_list = []

print("=== Équations d'ajustement ===")
for nom, y, c, m, ls in donnees:
    p, _ = curve_fit(modele, x, y, p0=p0_initial(x, y), maxfev=5000)
    params_list.append(p)
    print(f"{nom}: I(x) = {p[0]:.1f} x exp({p[1]:.4f} x x)  |  R2 = {r2(y, modele(x, *p)):.4f}")

fig, ax = plt.subplots(figsize=(10, 6))

ax.axhline(10000, color='black', linestyle='--', linewidth=1.2, label='10 000 lux')

for (nom, y, c, m, ls), p in zip(donnees, params_list):
    err = incertitude(y)
    ax.errorbar(x, y, yerr=err, label=nom, fmt=m, markersize=5,
                color=c, capsize=3, linestyle='', elinewidth=0.8)
    ax.plot(x_fit, modele(x_fit, *p), linestyle=ls, color=c, linewidth=1.5, alpha=0.8)

ax.set_xlabel("Distance (cm)", fontsize=20)
ax.set_ylabel("Intensite (lux)", fontsize=20)
ax.set_xlim(-1, 60)
ax.set_ylim(-1000, 48000)
ax.tick_params(labelsize=18)
ax.legend(fontsize=16)
plt.tight_layout()
plt.savefig("intensite_x_distance.png", bbox_inches='tight', dpi=600)
plt.show()