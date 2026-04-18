import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# PARAMÈTRES
# ============================================================
theta_zero = 67.42
ANGLE_MIN  = 0
ANGLE_MAX  = 70
sheet_name = "Essai1"
longueur   = ["35.435 mm", "55.783 mm", "76.131 mm", "96.479 mm", "127.001 mm"]
results    = []

vec_col = ["#B4A8C9", "#9982BB", "#7E48C9", "#450297", '#000000', "#FF5733"]

# ============================================================
# CHARGEMENT
# ============================================================
base_dir   = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "Projet_2_31_mars.xlsx")

if not os.path.exists(excel_path):
    raise FileNotFoundError(f"Fichier introuvable : {excel_path}")

df = pd.read_excel(excel_path, sheet_name=sheet_name, header=1)

angles_totaux = pd.to_numeric(df.iloc[:, 1], errors='coerce').values
angles        = angles_totaux - theta_zero

# ============================================================
# MODÈLE : A et C fixés, seul phi est libre
# sin(2x + phi) atteint son max quand 2x + phi = 90
# donc x_max = (90 - phi) / 2
# ============================================================
def sinusoidal_phi_only(x, phi):
    return 0.5 * np.sin(np.deg2rad(2.0 * x + phi)) + 0.5

fig, ax = plt.subplots(figsize=(13, 7))

# ============================================================
# BOUCLE PRINCIPALE
# ============================================================
for i, col in enumerate(longueur):

    y_total = pd.to_numeric(df[col], errors='coerce').values

    mask = ~np.isnan(y_total) & ~np.isnan(angles)
    if np.sum(mask) < 5:
        continue

    x = angles[mask]
    y = y_total[mask]

    # Normalisation min-max → y_norm ∈ [0, 1]
    # Justifie A = 0.5, C = 0.5 dans le modèle
    y_shifted = y - np.min(y)
    y_max_val = np.max(y_shifted)
    if y_max_val == 0:
        continue
    y_norm = y_shifted / y_max_val

    ax.scatter(x, y_norm, color=vec_col[i], s=25, alpha=0.55, zorder=3)

    # --------------------------------------------------------
    # ESTIMATION INITIALE DE phi à partir du max observé
    # On lisse y_norm avec une moyenne glissante pour éviter
    # qu'un point bruité isolé fausse l'estimation de phi_init
    # --------------------------------------------------------
    window = max(1, len(y_norm) // 10)   # fenêtre ~10% des points
    y_smooth_init = np.convolve(
        y_norm,
        np.ones(window) / window,
        mode='same'
    )
    x_max_obs = x[np.argmax(y_smooth_init)]
    phi_init  = 90.0 - 2.0 * x_max_obs

    # --------------------------------------------------------
    # POIDS GAUSSIEN : points proches du max comptent plus
    # sigma_gauss contrôle la largeur de la fenêtre de poids
    # On choisit ~25% de la plage angulaire totale
    # --------------------------------------------------------
    plage        = ANGLE_MAX - ANGLE_MIN
    sigma_gauss  = 0.25 * plage
    poids        = np.exp(-0.5 * ((x - x_max_obs) / sigma_gauss) ** 2)
    # curve_fit interprète sigma comme std du bruit →
    # on passe l'inverse des poids comme incertitude par point
    sigma_pts    = 1.0 / (poids + 1e-9)

    # --------------------------------------------------------
    # FIT : un seul paramètre libre → pcov est 1×1
    # --------------------------------------------------------
    try:
        popt, pcov = curve_fit(
            sinusoidal_phi_only,
            x,
            y_norm,
            p0=[phi_init],
            sigma=sigma_pts,
            absolute_sigma=False,   # on veut l'incertitude relative
            bounds=([-360], [360]),
            maxfev=20000
        )
    except RuntimeError:
        print(f"Curve fit échoué pour : {col}")
        continue

    phi = popt[0]

    # --------------------------------------------------------
    # θ_max et son incertitude
    # --------------------------------------------------------
    x_max = (90.0 - phi) / 2.0

    # Repliement dans [-90, 90]
    while x_max > 90:
        x_max -= 180
    while x_max < -90:
        x_max += 180

    dphi        = np.sqrt(pcov[0, 0])
    sigma_theta = 0.5 * dphi

    # --------------------------------------------------------
    # TRACÉ
    # --------------------------------------------------------
    x_smooth = np.linspace(ANGLE_MIN - 5, ANGLE_MAX + 5, 2000)
    y_smooth = sinusoidal_phi_only(x_smooth, phi)

    ax.plot(
            x_smooth,
            y_smooth,
            color=vec_col[i],
            linewidth=2,
            label=f"{col} | θ = {x_max:.2f} ± {sigma_theta:.2f}°"
        )

    ax.axvline(x_max, color=vec_col[i], linestyle='--', linewidth=1.3, alpha=0.7)

        # barres d'erreur
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

    print(f"{col} | θ = {x_max:.2f} ± {sigma_theta:.2f}°")
    results.append({
        "Longueur":        col,
        "Theta (deg)":     x_max,
        "Delta Theta (deg)": sigma_theta
    })

# ============================================================
# MISE EN PAGE
# ============================================================
ax.set_xlabel("Angle (degrés)", fontsize=16)
ax.set_ylabel("Intensité normlisée", fontsize=16)
ax.tick_params(axis='both', labelsize=14)
ax.set_xlim(ANGLE_MIN, ANGLE_MAX)
ax.set_ylim(-0.05, 1.15)
ax.legend(fontsize=14, loc='lower right', framealpha=0.92)
plt.tight_layout()


df_out   = pd.DataFrame(results)
csv_path = os.path.join(base_dir, "theta_glucose.csv")
df_out.to_csv(csv_path, index=False)


out_path = os.path.join(base_dir, "plot_glucose.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')

plt.show()