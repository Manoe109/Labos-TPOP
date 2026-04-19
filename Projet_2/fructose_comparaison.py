import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# PARAMÈTRES
theta_zero = 302.61
ANGLE_MIN  = -90
ANGLE_MAX  = 3

longueurs = ['25.261 mm', '50.696 mm', '76.131 mm', '101.566 mm', '127.001 mm']
results = []

vec_col = ["#0A2E0F", "#1B5E20", "#388E3C", "#81C784", "#AFDBB1", "#FFD600"]

base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

df = pd.read_excel(excel_path, sheet_name="Essai2", header=1)
df.columns = df.columns.astype(str).str.strip()

angles_raw = pd.to_numeric(df.iloc[:, 1], errors='coerce').values
angles = angles_raw - theta_zero

def sinusoidal(x, A, phi, C):
    return A * np.cos(np.deg2rad(2 * x + phi)) + C

fig, ax = plt.subplots(figsize=(13, 7))

colonnes_trouvees = {
    l: next((c for c in df.columns if l in c), None)
    for l in longueurs
}

for i, (longueur, col) in enumerate(colonnes_trouvees.items()):

    if col is None:
        print(f"Colonne introuvable pour {longueur}")
        continue

    y_raw = pd.to_numeric(df[col], errors='coerce').values

    mask = ~np.isnan(angles) & ~np.isnan(y_raw)

    if np.sum(mask) < 5:
        continue

    x = angles[mask]
    y = y_raw[mask]

    y_shifted = y - np.min(y)
    y_max = np.max(y_shifted)

    if y_max == 0:
        continue

    y_norm = y_shifted / y_max

    ax.scatter(x, y_norm, color=vec_col[i], s=25, alpha=0.55, zorder=3)

    try:
        p0 = [0.5, 0.0, 0.5]
        bounds = ([-1.5, -360, -0.5], [1.5, 360, 1.5])

        popt, pcov = curve_fit(
            sinusoidal, x, y_norm,
            p0=p0, bounds=bounds, maxfev=20000
        )

        A, phi, C = popt

        x_max = -phi / 2.0

        while x_max > 90:
            x_max -= 180
        while x_max < -90:
            x_max += 180

        dphi = np.sqrt(pcov[1, 1]) if pcov is not None else np.nan
        sigma_theta = 0.5 * dphi

        x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
        y_smooth = sinusoidal(x_smooth, *popt)

        ax.plot(
            x_smooth, y_smooth,
            color=vec_col[i], linewidth=2,
            label=f"{longueur} | θ = {x_max:.2f} ± {sigma_theta:.2f}°"
        )

        ax.axvline(x_max, color=vec_col[i], linestyle='--', linewidth=1.3, alpha=0.7)

        ax.errorbar(
            x_max, 1.0, xerr=sigma_theta,
            fmt='o', color=vec_col[i],
            capsize=10, markersize=5, zorder=10
        )

        print(f"{longueur} | θ = {x_max:.2f} ± {sigma_theta:.2f}°")

        results.append({
            "Longueur": longueur,
            "Theta (deg)": x_max,
            "Delta Theta (deg)": sigma_theta
        })

    except RuntimeError:
        print(f"Curve fit échoué pour : {longueur}")

# ============================================================
# PLOT FINAL
# ============================================================
ax.set_xlabel("Angle (°)", fontsize=18)
ax.set_ylabel("Intensité normalisée", fontsize=18)
ax.tick_params(axis='both', labelsize=16)
ax.set_xlim(ANGLE_MIN, ANGLE_MAX)
ax.axvline(0, color='black', linestyle='-', linewidth=1.5, zorder=2)
ax.set_ylim(-0.05, 1.15)
ax.legend(fontsize=15, loc='lower left', framealpha=0.92)
plt.tight_layout()

df_out = pd.DataFrame(results)
csv_path = os.path.join(base_dir, "theta_fructose.csv")
df_out.to_csv(csv_path, index=False)

out_path = os.path.join(base_dir, "plot_fructose.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
plt.show()