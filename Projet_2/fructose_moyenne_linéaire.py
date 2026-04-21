import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

base_dir = os.path.dirname(os.path.abspath(__file__))

longueur      = np.array([25.261, 50.696, 76.131, 101.566, 127.001]) / 100  # mm → dm
angle         = np.array([-10.20, -20.33, -30.56, -41.04, -51.63])          # °
concentration = 42.8 / 100  # g/100 mL → g/mL

# Variable composite c·ℓ (en dm·g/mL)
cl = concentration * longueur

def regression_lineaire(x, alpha_sp, b):
    return alpha_sp * x + b

popt, pcov = opt.curve_fit(regression_lineaire, cl, angle)
alpha_sp       = popt[0]
b              = popt[1]
sigma_alpha_sp = np.sqrt(pcov[0, 0])
sigma_b        = np.sqrt(pcov[1, 1])

print(f"Pouvoir rotatoire spécifique [α] = {alpha_sp:.1f} ± {sigma_alpha_sp:.1f} °·mL·dm⁻¹·g⁻¹")
print(f"Ordonnée à l'origine          b  = {b:.1f} ± {sigma_b:.1f} °")

x_fit = np.linspace(0, max(cl) * 1.1, 500)

plt.figure(figsize=(10, 6))
plt.scatter(cl, angle, color='black', s=50, label='Données expérimentales')
plt.plot(x_fit, alpha_sp * x_fit + b, color='black', linestyle='-', linewidth=1.5,
         label=f'Régression linéaire  $[\\alpha]$ = {alpha_sp:.1f} °·mL·dm⁻¹·g⁻¹,  b = {b:.1f}°')
plt.plot(x_fit, (alpha_sp - sigma_alpha_sp) * x_fit + (b - sigma_b),
         color="black", linestyle='--', linewidth=1, label='Régression avec incertitudes')
plt.plot(x_fit, (alpha_sp + sigma_alpha_sp) * x_fit + (b + sigma_b),
         color="black", linestyle='--', linewidth=1)
plt.xlabel(r"$c \cdot \ell$  (dm·g/mL)", fontsize=16)
plt.ylabel("Angle de rotation (°)", fontsize=16)
plt.tick_params(axis='both', labelsize=14)
plt.legend(fontsize=13)
plt.tight_layout()

out_path = os.path.join(base_dir, "plot_fructose_moyenne_lineaire.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
plt.show()