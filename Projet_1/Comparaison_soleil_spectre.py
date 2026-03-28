import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

dossier_script = os.path.dirname(os.path.abspath(__file__))

# --- Chargement du spectre solaire ---
fichier_xlsx = os.path.join(dossier_script, "Projet 1.xlsx")
spectre_solaire = pd.read_excel(fichier_xlsx, sheet_name="Spectre", skiprows=0)
x_soleil = spectre_solaire["Wavelength"].to_numpy()
y_soleil = spectre_solaire["Spectral irradiance"].to_numpy()

# --- Chargement du spectre de la lampe ---
fichier_csv = os.path.join(dossier_script, "spectre_at_bleu.csv")
spectre = pd.read_csv(fichier_csv)
x_lampe = spectre["lambda"].to_numpy()
y_lampe = np.sum([spectre[str(i)].to_numpy() for i in range(1, 11)], axis=0)

# --- Graphique ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# Axe gauche : comptes (lampe)
color_lampe = "#37379C"
ax1.plot(x_lampe, y_lampe, color=color_lampe, label="Lampe (comptes)")
ax1.set_xlabel("Longueur d'onde (nm)", fontsize=20)
ax1.set_ylabel("Compte", fontsize=20, color=color_lampe)
ax1.tick_params(axis='y', labelcolor=color_lampe, labelsize=18)
ax1.tick_params(axis='x', labelsize=18)

# Axe droit : irradiance (soleil)
color_soleil = "#FFA500"
ax2 = ax1.twinx()
ax2.plot(x_soleil, y_soleil, color=color_soleil, label="Spectre solaire (irradiance)")
ax2.set_ylabel("Irradiance (W/m²/nm)", fontsize=20, color=color_soleil)
ax2.tick_params(axis='y', labelcolor=color_soleil, labelsize=18)

# Légende combinée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=14)

plt.tight_layout()
plt.savefig(os.path.join(dossier_script, "spectre_combine.png"), bbox_inches='tight', dpi=600)
plt.show()