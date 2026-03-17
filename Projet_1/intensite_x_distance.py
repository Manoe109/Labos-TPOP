import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "Projet 1.xlsx")

spectre = pd.read_excel(fichier_csv, sheet_name="Obj2", skiprows=1)

x = spectre["Distance (cm)"].to_numpy()

y1 = spectre["AT"].to_numpy()
y2 = spectre["AC"].to_numpy()
y3 = spectre["MEN"].to_numpy()
y4 = spectre["MN"].to_numpy()


plt.figure(figsize=(10, 6))
plt.plot(x, y1, label="intensité AT", color="#800080")
plt.plot(x, y2, label="intensité AC", color="#007980")
plt.plot(x, y3, label="intensité MEN", color="#008000")
plt.plot(x, y4, label="intensité MN", color="#FFA500")
plt.xlabel("Distance (cm)")
plt.ylabel("Intensité (lux)")
plt.show()
