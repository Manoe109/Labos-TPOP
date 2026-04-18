import numpy as np
import os
import pandas as pd
import sympy as sp

#donnes volumes de mesure + masses et volumes dilution
volumes_glucose = np.array([7, 11, 15, 19, 25])
volumes_fructose = np.array([5, 10, 15, 20, 25])
volumes_melange = np.array([15, 25])
masses_dilution = np.array([10.7, 45.45])
volumes_dilution = np.array([25, 100])

#theta et delta theta glucose
dossier_glucose = os.path.dirname(os.path.abspath(__file__))
fichier_csv_glucose = os.path.join(dossier_glucose, "theta_glucose.csv")
valeurs_glucose = pd.read_csv(fichier_csv_glucose)
theta_glucose = valeurs_glucose["Theta (deg)"].to_numpy()
delta_theta_glucose = valeurs_glucose["Delta Theta (deg)"].to_numpy()

#theta et delta theta fructose
dossier_fructose = os.path.dirname(os.path.abspath(__file__))
fichier_csv_fructose = os.path.join(dossier_fructose, "theta_fructose.csv")
valeurs_fructose = pd.read_csv(fichier_csv_fructose)
theta_fructose = valeurs_fructose["Theta (deg)"].to_numpy()
delta_theta_fructose = valeurs_fructose["Delta Theta (deg)"].to_numpy()

#theta et delta theta mélange
dossier_melange = os.path.dirname(os.path.abspath(__file__))
fichier_csv_melange = os.path.join(dossier_melange, "theta_melange.csv")
valeurs_melange = pd.read_csv(fichier_csv_melange)
theta_melange = valeurs_melange["Theta (deg)"].to_numpy()
delta_theta_melange = valeurs_melange["Delta Theta (deg)"].to_numpy()

def longueur(v):
    l = 10 + 5.087 * (v-2) #incertitude sur 10 : 2mm, incertitude sur v : 0.5 ml, incertitude sur 5.08 : 0.043
    return l

def incertitude_longueur(v):
    a = 10
    delta_a = 0.2
    b = 5.087 
    delta_b = 0.043
    c = v
    delta_c = 0.5
    delta_l = np.sqrt(delta_a**2 + (b * delta_c)**2 + (c * delta_b)**2)
    return delta_l

def concentration(m, v):
    c = m / v #incertitude sur m : 0.1 g, incertitude sur v : 0.5 ml
    return c

def concentration_incertitude(m, v):
    delta_m = 0.1
    delta_v = 0.5
    c = concentration(m, v)
    delta_c = c * np.sqrt((delta_m / m)**2 + (delta_v / v)**2)
    return delta_c


alpha_moy_glucose = np.mean(theta_glucose / (longueur(volumes_glucose) * concentration(masses_dilution, volumes_dilution)[1]))
alpha_moy_fructose = np.mean(theta_fructose / (longueur(volumes_fructose) * concentration(masses_dilution, volumes_dilution)[0]))


def incertitude_alpha_glucose(conc, d_conc, angle, d_angle, long, d_long):
    incertitude = 0
    for i, j in enumerate(angle):
        terme1 = ((1/5) * (1 / (conc[1])) * (d_angle[i] / long[i]))**2
        terme2 = ((1/5) * (1 / (conc[1])) * (angle[i] * d_long[i] / (long[i]**2)))**2
        terme3 = ((1/5) * (d_conc[1] / (conc[1]**2)) * (angle[i] / long[i]))**2
        incertitude += terme1 + terme2 + terme3

    return np.sqrt(incertitude)

def incertitude_alpha_fructose(conc, d_conc, angle, d_angle, long, d_long):
    incertitude = 0
    for i, j in enumerate(angle):
        terme1 = ((1 / (5 * conc[0])) * (d_angle[i] / long[i]))**2
        terme2 = ((1 / (5 * conc[0])) * (angle[i] * d_long[i] / (long[i]**2)))**2
        terme3 = ((d_conc[0] / (5 * conc[0]**2)) * (angle[i] / long[i]))**2
        incertitude += terme1 + terme2 + terme3

    return np.sqrt(incertitude)

incertitude_finale_glucose = np.sqrt(((incertitude_alpha_glucose(concentration(masses_dilution, volumes_dilution), 
        concentration_incertitude(masses_dilution, volumes_dilution), theta_glucose, delta_theta_glucose, 
        longueur(volumes_glucose), 
        incertitude_longueur(volumes_glucose)))**2 / alpha_moy_glucose**2 + 1.03**2 / 67.42**2))
incertitude_finale_fructose = np.sqrt((incertitude_alpha_fructose(concentration(masses_dilution, volumes_dilution), 
        concentration_incertitude(masses_dilution, volumes_dilution), theta_fructose, delta_theta_fructose, 
        longueur(volumes_fructose), 
        incertitude_longueur(volumes_fructose)))**2 / alpha_moy_fructose**2 + 2**2 / 302.61**2 )


matrix = sp.Matrix([
    [(longueur(volumes_melange)[0] * alpha_moy_glucose),
     (longueur(volumes_melange)[0] * alpha_moy_fructose),
     theta_melange[0]],

    [(longueur(volumes_melange)[1] * alpha_moy_glucose),
     (longueur(volumes_melange)[1] * alpha_moy_fructose),
     theta_melange[1]]
])

a = matrix.rref(pivots=False)


print(f"longueurs glucose : {longueur(volumes_glucose)} mm")
print(f"longueurs fructose : {longueur(volumes_fructose)} mm")
print(f"Longueurs mélange : {longueur(volumes_melange)} mm")

print(f"Alpha moyen glucose : {(alpha_moy_glucose)} °/(mm·g/ml)")
print(f"Incertitude alpha glucose : {incertitude_finale_glucose} °/(mm·g/ml)")


print(f"Alpha moyen glucose : {(alpha_moy_fructose)} °/(mm·g/ml)")
print(f"Incertitude alpha fructose : {incertitude_finale_fructose} °/(mm·g/ml)")
