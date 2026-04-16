import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# PARAMÈTRES — faciles à modifier
# ============================================================
theta_zero = 0
ANGLE_MIN  = 0
ANGLE_MAX  = 360
# ============================================================

base_dir   = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

df = pd.read_excel(excel_path, sheet_name="Essai2", header=1)

angles_raw = df.iloc[:, 1].values.astype(float)

mask    = (angles_raw >= 180) & (angles_raw <= 360)
x_raw   = angles_raw[mask]
x_shift = x_raw - theta_zero

def sinusoidal(x, A, phi, C):
    return A * np.cos(np.deg2rad(2 * x + phi)) + C

fig, ax = plt.subplots(figsize=(13, 7))

# Trouver la colonne 'vide' par nom
vide_candidates = [c for c in df.columns if str(c).strip().lower() == 'vide']
if not vide_candidates:
    raise ValueError(f"Colonne 'vide' introuvable. Colonnes disponibles : {df.columns.tolist()}")

col   = vide_candidates[0]
color = '#000000'

y_raw      = pd.to_numeric(df[col], errors='coerce').values
y_filtered = y_raw[mask]

valid = ~np.isnan(y_filtered)
if valid.sum() < 5:
    raise ValueError(f"Pas assez de points valides dans la colonne '{col}' ({valid.sum()} points).")

x = x_shift[valid]
y = y_filtered[valid]

y_shifted = y - np.min(y)
y_norm    = y_shifted / np.max(y_shifted)

ax.scatter(x, y_norm, color=color, s=25, alpha=0.55, zorder=3)

p0     = [0.5, 0.0, 0.5]
bounds = ([-1.5, -360, -0.5], [1.5, 360, 1.5])

popt, pcov = curve_fit(sinusoidal, x, y_norm, p0=p0, bounds=bounds, maxfev=20000)
A, phi, C = popt

x_max = -phi / 2.0
while x_max < 180:
    x_max += 180
while x_max > 360:
    x_max -= 180

try:
    dphi        = np.sqrt(pcov[1, 1]) if pcov is not None else np.nan
    sigma_theta = dphi / 2.0
except Exception:
    sigma_theta = np.nan

x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
y_smooth = sinusoidal(x_smooth, *popt)

legend_label = f"Vide  |  θ_max = {x_max:.2f} ± {sigma_theta:.2f}°"
ax.plot(x_smooth, y_smooth, color=color, linewidth=2, label=legend_label)
ax.axvline(x_max, color='red', linestyle='--', linewidth=1.2, alpha=0.8, label=f"θ_max = {x_max:.2f}°")

print(f"Vide  |  θ_max = {x_max:.2f} ± {sigma_theta:.2f}°")

ax.axvline(0, color='gray', linewidth=1.2, linestyle='-', alpha=0.5, label='θ − θ₀ = 0°')
ax.set_xlabel("Angle θ − θ₀  (degrés)", fontsize=13)
ax.set_ylabel("Courant normalisé (u.a.)", fontsize=13)
ax.set_title("Courant à vide — Essai 2", fontsize=13)
ax.legend(fontsize=9, loc='upper right', framealpha=0.92)
ax.grid(True, alpha=0.3)
ax.set_xlim(ANGLE_MIN, ANGLE_MAX)
ax.set_ylim(-0.05, 1.15)

plt.tight_layout()

out_path = os.path.join(base_dir, "plot_fructose_vide.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')

plt.show()
