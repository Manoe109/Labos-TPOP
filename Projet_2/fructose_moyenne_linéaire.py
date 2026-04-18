import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

base_dir = os.path.dirname(os.path.abspath(__file__))

longueur = np.array([25.261, 50.696, 76.131, 101.566, 127.001] )     # mm
angle = np.array([-10.20, -20.33, -30.56, -41.04, -51.63])  # °
concentration = 42.8  # g/100 mL

# Variable composite c·ℓ (en mm·g/100mL)
cl = concentration * longueur

def regression_lineaire(x, alpha_sp, b):
    return alpha_sp * x + b

popt, pcov = opt.curve_fit(regression_lineaire, cl, angle)
alpha_sp       = popt[0]
b              = popt[1]
sigma_alpha_sp = np.sqrt(pcov[0, 0])
sigma_b        = np.sqrt(pcov[1, 1])

print(f"Pouvoir rotatoire spécifique [α] = {alpha_sp:.6f} ± {sigma_alpha_sp:.6f} °·mL·mm⁻¹·g⁻¹")
print(f"Ordonnée à l'origine          b  = {b:.6f} ± {sigma_b:.6f} °")

cl_fit    = np.linspace(min(cl), max(cl), 100)
angle_fit = alpha_sp * cl_fit + b

plt.figure(figsize=(10, 6))
plt.scatter(cl, angle, color='black', s=50, label='Données expérimentales')
plt.plot(cl_fit, angle_fit, color='black', linestyle='-', linewidth=2,
         label=f'Régression linéaire  $[\\alpha]$ = {alpha_sp:.6f} °·mL·mm⁻¹·g⁻¹,  b = {b:.4f}°')
plt.xlabel(f"$c \cdot \ell$  (mm·g/100 mL)", fontsize=14)
plt.ylabel("Angle de rotation (°)", fontsize=14)
plt.legend(fontsize=11)
plt.tight_layout()

out_path = os.path.join(base_dir, "plot_fructose_moyenne_lineaire.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
plt.show()