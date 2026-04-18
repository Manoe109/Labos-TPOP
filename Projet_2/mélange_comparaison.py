import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

theta_zero   = 121.22
ANGLE_MIN    = -180
ANGLE_MAX    = 180  
sheet_name   = "Essai3"
longueur     = ['76.131 mm', '127.001 mm'] 
results = []

base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

if not os.path.exists(excel_path):
    raise FileNotFoundError(f"Fichier introuvable : {excel_path}")

df = pd.read_excel(excel_path, sheet_name=sheet_name, header=1)

angles_totaux = pd.to_numeric(df.iloc[:, 1], errors='coerce').values
angles = angles_totaux - theta_zero

def sinusoidal(x, A, B, phi, C):
    return A * np.sin(np.deg2rad(B * x + phi)) + C

vec_col = ["#8861CB", "#3D275F"]

fig, ax = plt.subplots(figsize=(13, 7))

for i, col in enumerate(longueur):

    y_total = pd.to_numeric(df[col], errors='coerce').values

    mask = ~np.isnan(y_total) & ~np.isnan(angles)

    if np.sum(mask) < 5:
        continue

    x = angles[mask]
    y = y_total[mask]

    y_shifted = y - np.min(y)
    y_max = np.max(y_shifted)
    if y_max == 0:
        continue
    y_norm = y_shifted / y_max

    ax.scatter(x, y_norm, color=vec_col[i], s=25, zorder=3)

    p0 = [0.5, 2, 0.0, 0.5]
    bounds = ([-1.5, 0, -360, -0.5], [1.5, 10, 360, 1.5])

    popt, pcov = curve_fit(
        sinusoidal,
        x,
        y_norm,
        p0=p0,
        bounds=bounds,
        maxfev=20000
    )

    A, B, phi, C = popt

    x_max = (90 - phi) / B

    while x_max > 90:
        x_max -= 180
    while x_max < -90:
        x_max += 180

    try:
        dA = np.sqrt(pcov[0, 0])
        dB = np.sqrt(pcov[1, 1])

        sigma_theta = abs(x_max) * np.sqrt(
            (dA / (abs(A) + 1e-12))**2 +
            (dB / (abs(B) + 1e-12))**2
        )
    except:
        sigma_theta = np.nan

    x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
    y_smooth = sinusoidal(x_smooth, *popt)

    ax.plot(
        x_smooth,
        y_smooth,
        color=vec_col[i],
        linewidth=2,
        label=f"{longueur[i]} | θ = {x_max:.2f} ± {sigma_theta:.2f}°"
    )
    ax.errorbar(
        x_max,
        1.0,
        xerr=sigma_theta,
        fmt='o',
        color=vec_col[i],
        capsize=10,
        markersize=5,
        zorder=10
    )
    results.append({
        "Longueur": longueur,
        "Theta (deg)": x_max,
        "Delta Theta (deg)": sigma_theta
    })

    ax.axvline(x_max, color=vec_col[i], linestyle='--', linewidth=1.5)

ax.set_xlabel("Angle (degrés)", fontsize=16)
ax.set_ylabel("Intensité normalisée", fontsize=16)
ax.set_xlim(-90, 90)
ax.set_ylim(-0.05, 1.05)

ax.legend(fontsize=12, loc='upper right', framealpha=0.92)

plt.tight_layout()

df_out   = pd.DataFrame(results)
csv_path = os.path.join(base_dir, "theta_melange.csv")
df_out.to_csv(csv_path, index=False)


out_path = os.path.join(base_dir, "plot_melange.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')

plt.show()
