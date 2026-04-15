import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ANGLE_MIN = 0
ANGLE_MAX = 100
sheet_name = "Essai1"

base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

df = pd.read_excel(excel_path, sheet_name=sheet_name, header=1)
df.columns = df.columns.astype(str).str.strip().str.lower()

col = "vide"

if col not in df.columns:
    raise ValueError(f"Colonne '{col}' introuvable")

angles = pd.to_numeric(df["angle"], errors='coerce').values
y_total = pd.to_numeric(df[col], errors='coerce').values

mask = ~np.isnan(y_total) & ~np.isnan(angles)
x = angles[mask]
y = y_total[mask]

y_shifted = y - np.min(y)
y_norm = y_shifted / np.max(y_shifted)

def sinusoidal(x, A, B, phi, C):
    return A * np.sin(np.deg2rad(B * x + phi)) + C

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

print(f"y = {A:.3f} * sin({B:.3f} * x + {phi:.1f}) + {C:.3f}")
print(f"θ_max = {x_max:.2f} ± {sigma_theta:.2f}°")

x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
y_smooth = sinusoidal(x_smooth, *popt)

plt.figure(figsize=(10, 6))
plt.scatter(x, y_norm, s=25, label="Données (vide)")
plt.plot(x_smooth, y_smooth, linewidth=2, label=f"Fit | θ = {x_max:.2f}°")
plt.axvline(x_max, linestyle='--')

plt.xlabel("Angle (degrés)")
plt.ylabel("Intensité normalisée")
plt.xlim(ANGLE_MIN, ANGLE_MAX)
plt.ylim(-0.05, 1.15)
plt.legend()
plt.grid()

out_path = os.path.join(base_dir, "plot_glucose_vide.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')

plt.show()