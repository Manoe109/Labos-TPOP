import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# ============================================================
# PARAMÈTRES — faciles à modifier
# ============================================================
theta_zero = 302.61
ANGLE_MIN  = -130
ANGLE_MAX  =   80
# ============================================================

base_dir   = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

df = pd.read_excel(excel_path, sheet_name="Essai2", header=1)

angles_raw = df.iloc[:, 1].values.astype(float)

mask = (angles_raw >= 180) & (angles_raw <= 360)
x_raw   = angles_raw[mask]
x_shift = x_raw - theta_zero


def sinusoidal(x, A, phi, C):
    return A * np.cos(np.deg2rad(2 * x + phi)) + C

vec_col = ["#B4A8C9", "#9982BB", "#916AC9", "#5A4574", '#000000', "#FF5733"]

fig, ax = plt.subplots(figsize=(13, 7))

for i, col in enumerate(df.columns[2:2+len(vec_col)]):

    y_raw      = pd.to_numeric(df[col], errors='coerce').values
    y_filtered = y_raw[mask]

    valid = ~np.isnan(y_filtered)
    if valid.sum() < 5:
        continue

    x = x_shift[valid]
    y = y_filtered[valid]

    y_shifted = y - np.min(y)
    y_max = np.max(y_shifted)
    if y_max == 0:
        continue
    y_norm = y_shifted / y_max

    ax.scatter(x, y_norm, color=vec_col[i], s=25, alpha=0.55, zorder=3)

    try:
        p0     = [0.5, 0.0, 0.5]
        bounds = ([-1.5, -360, -0.5], [1.5, 360, 1.5])

        popt, pcov = curve_fit(
            sinusoidal,
            x,
            y_norm,
            p0=p0,
            bounds=bounds,
            maxfev=20000
        )

        A, phi, C = popt

        # ============================================================
        # θ max
        # ============================================================
        x_max = -phi / 2.0

        while x_max > 90:
            x_max -= 180
        while x_max < -90:
            x_max += 180

        # ============================================================
        # INCERTITUDE (ajout code #1 adapté)
        # ============================================================
        try:
            dA = np.sqrt(pcov[0, 0]) if pcov is not None else np.nan
            dphi = np.sqrt(pcov[1, 1]) if pcov is not None else np.nan

            sigma_theta = abs(x_max) * np.sqrt(
                (dphi / (abs(phi) + 1e-12))**2
            )
        except:
            sigma_theta = np.nan

        # ============================================================

        x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
        y_smooth = sinusoidal(x_smooth, *popt)

        legend_label = f"{col} mm  |  θ_max = {x_max:.2f} ± {sigma_theta:.2f}°"
        ax.plot(x_smooth, y_smooth, color=vec_col[i], linewidth=2, label=legend_label)

        ax.axvline(x_max, color=vec_col[i], linestyle='--', linewidth=0.7, alpha=0.4)

    except RuntimeError:
        print(f"Curve fit échoué pour : {col}")

    print(f"{col} mm  |  θ_max = {x_max:.2f} ± {sigma_theta:.2f}°")

ax.axvline(0, color='black', linewidth=1.2, linestyle='-', alpha=0.5, label='θ − θ₀ = 0°')
ax.set_xlabel("Angle θ − θ₀  (degrés)", fontsize=13)
ax.set_ylabel("Courant normalisé (u.a.)", fontsize=13)
ax.legend(fontsize=8.5, loc='upper right', framealpha=0.92)
ax.grid(True, alpha=0.3)
ax.set_xlim(ANGLE_MIN, ANGLE_MAX)
ax.set_ylim(-0.05, 1.15)

plt.tight_layout()
plt.show()

out_path = os.path.join(base_dir, "plot_fructose.png")
# plt.savefig(out_path, dpi=150, bbox_inches='tight')