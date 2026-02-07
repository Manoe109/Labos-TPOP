import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- Configuration des chemins ---
# Récupère le dossier où se trouve le script actuel
dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_xlsx = os.path.join(dossier_script, "polarisation.xlsx")

# --- Lecture des données ---
# Expérience A
pol = pd.read_excel(fichier_xlsx, sheet_name=0)
x = pol["angle"].to_numpy()
y1 = pol["intensité_te"].to_numpy()
y2 = pol["intensité_tm"].to_numpy()

# Expérience D
exp_D = pd.read_excel(fichier_xlsx, sheet_name=1)
xd = exp_D["angle"].to_numpy()
yd = exp_D["intensité"].to_numpy()

# Expérience E
exp_e = pd.read_excel(fichier_xlsx, sheet_name=2)
xe = exp_e["angle"].to_numpy()
ye1 = exp_e["intensité 22.5"].to_numpy()
ye2 = exp_e["intensité 44.5"].to_numpy()


# --- Figure 1: Réflectance (hypothèse I_max = 0.9 * I0) ---
a = plt.figure(figsize=(10, 6))

# Angle de Brewster / indice (estimation utilisée)
teta_Brewster = 55
marge_erreur_tB = 1
plt.axvline(teta_Brewster, color='green', linestyle='--', label=f"Angle de Brewster = {teta_Brewster}° ± {marge_erreur_tB}°")
n1 = 1.0
# estimation de n2 à partir de l'angle de Brewster
n2 = n1 * np.tan(np.radians(teta_Brewster))
print("Indice de réfraction du plexiglas (estimé):", n2)


# Hypothèse: I_max observé correspond à 0.9 * I0 réel
I_max_obs = max(y1.max(), y2.max()) if (y1.size and y2.size) else 1.0
I0_assumed = I_max_obs / 0.9


# Calcul de la réflectance mesurée (fraction)
R_te_meas = y1 / I0_assumed
R_tm_meas = y2 / I0_assumed

# Tracé : réflectance mesurée (%)
plt.plot(x, 100 * R_te_meas, linestyle='-.', linewidth=1, label='Polarisation TE', color= "grey")
plt.plot(x, 100 * R_tm_meas, linestyle='-', linewidth=1, label='Polarisation TM', color="black")

plt.rcParams.update({"font.family": "serif", "font.size": 16})

plt.xlabel("Angle d'incidence (°)", fontsize=20, fontfamily="serif")
plt.ylabel("Réflectance (%)", fontsize=20, fontfamily="serif")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#plt.legend(fontsize=14, loc='upper left')
plt.ylim(0, 95)
plt.xlim(8, max(x) + 2)

# ensure legend is drawn on the current axis
ax = plt.gca()
ax.legend(loc='upper left', fontsize=18)

plt.tight_layout()
# Sauvegarde avant l'affichage
a.savefig(os.path.join(dossier_script, "graph_1.pdf"), bbox_inches='tight')
plt.show()

# --- Figure 2: Deux polariseurs ---
b = plt.figure(figsize=(10, 6))
plt.plot(xd, yd, linestyle='-', linewidth=1, label='Intensité transmise', color="#898D8D")

plt.xlabel("Angle (°)", fontsize=20)
plt.ylabel("Intensité", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=16)
plt.title("D. Intensité transmise entre 2 polariseurs", fontsize=22)

# Sauvegarde avant l'affichage
b.savefig(os.path.join(dossier_script, "graph_2.pdf"), bbox_inches='tight')
#plt.show()


# --- Figure 3: Lame demi-onde ---
f = plt.figure(figsize=(10, 6))
plt.plot(xe, ye1, marker='o', linestyle=' ', label='Intensité 22,5°', color="#898D8D")
plt.plot(xe, ye2, marker='x', linestyle=' ', label='Intensité 45°', color="black")

plt.xlabel("Angle (°)", fontsize=20)
plt.ylabel("Intensité", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=16)
plt.title("E. Intensité transmise pour une lame DEMI onde", fontsize=22)

# Sauvegarde avant l'affichage
f.savefig(os.path.join(dossier_script, "graph_3.pdf"), bbox_inches='tight')
#plt.show()

#print(f"Sauvegarde terminée dans : {dossier_script}")