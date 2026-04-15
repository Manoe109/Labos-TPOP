import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

base_dir = os.path.dirname(os.path.abspath(__file__))

longueur      = np.array([35.43, 60.78, 86.31, 111.84, 137.18])     # mm
angle         = np.array([-10.11, -20.48, -30.53, -40.85, -52.05])  # °
concentration = 42.8  # g/100 mL

# Variable composite c·ℓ (en mm·g/100mL)
cl = concentration * longueur

def regression_lineaire(x, alpha_sp):
    return alpha_sp * x

popt, pcov = opt.curve_fit(regression_lineaire, cl, angle)
alpha_sp       = popt[0]
sigma_alpha_sp = np.sqrt(pcov[0, 0])

print(f"Pouvoir rotatoire spécifique [α] = {alpha_sp:.6f} ± {sigma_alpha_sp:.6f} °·mL·mm⁻¹·g⁻¹")

cl_fit    = np.linspace(min(cl), max(cl), 100)
angle_fit = alpha_sp * cl_fit

plt.figure(figsize=(10, 6))
plt.scatter(cl, angle, color='black', s=50, label='Données expérimentales')
plt.plot(cl_fit, angle_fit, color='black', linestyle='-', linewidth=2,
         label=f'Régression linéaire  $[\\alpha]$ = {alpha_sp:.6f} °·mL·mm⁻¹·g⁻¹')
plt.xlabel(r"$c \cdot \ell$  (mm·g/100 mL)", fontsize=14)
plt.ylabel("Angle de rotation (°)", fontsize=14)
plt.legend(fontsize=11)
plt.tight_layout()

out_path = os.path.join(base_dir, "plot_fructose_moyenne_lineaire.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
plt.show()