import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 1. Gestion du chemin du fichier
file_name = '24janvierV1.csv'  # ou 'data.csv' selon le nom réel du fichier
file_path = os.path.join(os.path.dirname(__file__), file_name)

# 2. Chargement des données
df = pd.read_csv(file_path)
x_data = df.iloc[:, 0]
y_raw = df.iloc[:, 1]

# 3. Traitement du signal
# Centrage sur l'origine définie par tes points de repère
target_center = (4.027 + 2.3) / 2
idx_center = (x_data - target_center).abs().idxmin()
x_centered = x_data - x_data[idx_center]

# Normalisation entre -0.1 et 1
y_normalized = (y_raw - y_raw.min()) / (y_raw.max() - y_raw.min())  # 0 à 1
y_final = y_normalized * 1.1 - 0.1  # Rescale pour avoir -0.1 à 1

# --- PARAMÈTRES PHYSIQUES ---
lambda_m = 650e-9 
d_G_m = (110 - 57.5) / 100 

# --- CALCUL DES PARAMÈTRES (a et b) ---
m_diff = 1 
x_min_diff_cm = 0.9 
theta_min_diff = np.arctan((x_min_diff_cm/100) / d_G_m)
a = (m_diff * lambda_m) / np.sin(theta_min_diff)

m_int = 1
x_max_int_cm = 0.1428 
theta_max_int = np.arctan((x_max_int_cm/100) / d_G_m)
b = (m_int * lambda_m) / np.sin(theta_max_int)

# Affichage des résultats
print(f"Largeur de fente (a) : {a*1e3:.4f} mm")
print(f"Distance entre fentes (b) : {b*1e3:.4f} mm")

# 4. Création de la figure
plt.rcParams.update({"font.family": "serif", "font.size": 11})
f, ax = plt.subplots(figsize=(8, 5))

# Affichage des données expérimentales
ax.plot(x_centered, y_final, color='black', linewidth=1)

# Configuration des axes
ax.set_xlabel(r'Distance au centre $x$ (cm)')
ax.set_ylabel(r'Intensité relative')

# Ajustement des limites (pas de titre, échelle Y commence à -0.1)
limit = max(abs(x_centered.min()), abs(x_centered.max()))
ax.set_xlim(-limit, limit)
ax.set_ylim(-0.1, 1.05) 

plt.tight_layout()
plt.show()

# Sauvegarde
f.savefig("graph_1.pdf", bbox_inches='tight')
f.savefig("graph_1.png", bbox_inches='tight', dpi=600)