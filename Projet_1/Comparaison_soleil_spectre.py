import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

dossier_script = os.path.dirname(os.path.abspath(__file__))


# charger spectre solaire
fichier_xlsx = os.path.join(dossier_script, "Projet 1.xlsx")
spectre_solaire = pd.read_excel(fichier_xlsx, sheet_name="Spectre", skiprows=0)
x_soleil = spectre_solaire["Wavelength"].to_numpy()
y_soleil = spectre_solaire["Spectral irradiance"].to_numpy()

# charger spectre lampe
fichier_csv = os.path.join(dossier_script, "spectre_at_bleu.csv")
spectre = pd.read_csv(fichier_csv)
x_lampe = spectre["lambda"].to_numpy()
y_lampe = np.sum([spectre[str(i)].to_numpy() for i in range(1, 11)], axis=0)

# normalisation spectres
y_soleil_norm = y_soleil / np.max(y_soleil)
y_lampe_norm = y_lampe / np.max(y_lampe)

# graphique
fig, ax1 = plt.subplots(figsize=(10, 6))

# axe compte
couleur_lampe = "#696969"
ax1.plot(x_lampe, y_lampe_norm, color=couleur_lampe, label="Intensité de la lampe")
ax1.set_xlabel("Longueur d'onde (nm)", fontsize=20)
ax1.set_ylabel("Intensité normalisée", fontsize=20, color=couleur_lampe)
ax1.tick_params(axis='y', labelcolor=couleur_lampe, labelsize=18)
ax1.tick_params(axis='x', labelsize=18)

# axe irradiance
couleur_soleil = "#121212"
ax2 = ax1.twinx()
ax2.plot(x_soleil, y_soleil_norm, color=couleur_soleil, label="Irradiance solaire")
ax2.set_ylabel("Irradiance normalisée", fontsize=20, color=couleur_soleil)
ax2.tick_params(axis='y', labelcolor=couleur_soleil, labelsize=18)

# légende
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=14)

plt.tight_layout()
plt.savefig(os.path.join(dossier_script, "spectre_combine.png"), bbox_inches='tight', dpi=600)
plt.show()