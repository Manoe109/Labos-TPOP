import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

lampe_2 = "black"

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "spectre_men.csv")

spectre = pd.read_csv(fichier_csv)
x = spectre["lambda"].to_numpy()
y = np.sum([spectre[str(i)].to_numpy() for i in range(1, 11)], axis=0)

# Normalisation
y_norm = y / np.max(y)

# Raies du mercure (NIST)
raies_hg = [404.7, 435.9, 545.9, 576.9]

# Pics du phosphore triphosphore CFL (Jüstel et al., 1998)
raies_phosphore = [486.9, 611.4]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y_norm, color=lampe_2, linewidth=1.5, label="Spectre mesuré (lampe 2)")

for lam in raies_hg:
    ax.axvline(lam, color='red', linewidth=1.2, linestyle='--', alpha=0.8,
               label='Mercure (Hg)' if lam == raies_hg[0] else '')
    ax.text(lam + 2, 0.97, f"{lam:.0f} nm", fontsize=11, color='red',
            rotation=90, va='top')

for lam in raies_phosphore:
    ax.axvline(lam, color='blue', linewidth=1.2, linestyle='--', alpha=0.8,
               label='Phosphore (P)' if lam == raies_phosphore[0] else '')
    ax.text(lam + 2, 0.97, f"{lam:.0f} nm", fontsize=11, color='blue',
            rotation=90, va='top')

ax.set_xlabel("Longueur d'onde (nm)", fontsize=20)
ax.set_ylabel("Compte normalisé", fontsize=20)
ax.set_xlim(200, 900)
ax.set_ylim(-0.05, 1.1)
ax.tick_params(labelsize=18)
ax.legend(fontsize=14)
plt.tight_layout()
plt.savefig("spectres_individuels2_V3.png", bbox_inches='tight', dpi=600)
plt.show()