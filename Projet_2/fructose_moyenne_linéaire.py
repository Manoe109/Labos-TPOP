import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

base_dir   = os.path.dirname(os.path.abspath(__file__))

longueur = np.array([35.43, 60.78, 86.31, 111.84, 137.18])
angle = np.array([-10.11, -20.48, -30.53, -40.85, -52.05])
concentration = np.array([42.8 for i in range(len(longueur))])

alpha = angle / (longueur * concentration)
print("Alpha (°/(mm·g/L)) :", alpha)

def regression_lineaire(x, a):
    return a * x

popt, pcov = opt.curve_fit(regression_lineaire, longueur, angle)
a = popt[0]
print(f"Coefficients de la régression linéaire : a = {a:.6f}")

longueur_fit = np.linspace(min(longueur), max(longueur), 100)
angle_fit = a * longueur_fit

alpha_moy = np.mean(alpha)
print(f"Alpha moyen : {alpha_moy:.6f} °/(mm·g/ml)")

plt.figure(figsize=(10, 6))
plt.scatter(longueur, angle, color='black', s=50, label='Données expérimentales')
plt.plot(longueur_fit, angle_fit, color='black', linestyle='-', linewidth=2, label='Régression linéaire')
plt.xlabel("Longueur (mm)", fontsize=14)
plt.ylabel("Angle (°)", fontsize=14)
plt.legend()

out_path = os.path.join(base_dir, "plot_fructose_moyenne_lineaire.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')

plt.show()