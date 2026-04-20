import numpy as np

# Pouvoirs rotatoires spécifiques mesurés (°·(100 mL)·mm⁻¹·g⁻¹)
alpha_glucose  =  0.005508
alpha_fructose = -0.009514

# Concentrations effectives dans le mélange (g/100 mL)
c_glucose  = 25.97
c_fructose = 18.34

# Longueurs testées (mm)
longueurs = np.array([76.131, 127.001])

# Facteur combiné
facteur = alpha_glucose * c_glucose + alpha_fructose * c_fructose
print(f"Facteur combiné [α_g·c_g + α_f·c_f] = {facteur:.6f} °/mm")

# Angles attendus
for l in longueurs:
    theta_attendu = facteur * l
    print(f"ℓ = {l:.3f} mm → θ attendu = {theta_attendu:.3f}°")

# Comparaison avec les angles mesurés
print()
theta_mesures = np.array([-5.99, -7.54])
theta_attendus = facteur * longueurs

print(f"{'Longueur':>12} {'θ attendu':>12} {'θ mesuré':>12} {'Écart':>10}")
for l, ta, tm in zip(longueurs, theta_attendus, theta_mesures):
    print(f"{l:>12.3f} {ta:>12.3f} {tm:>12.3f} {tm - ta:>10.3f}")