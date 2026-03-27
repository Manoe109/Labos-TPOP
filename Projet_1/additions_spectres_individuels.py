import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

#lampe 1 : MN
#lampe 2 : MEN
#lampe 3 : AC
#lampe 4 : AT

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "spectre_mn.csv")
duree_exposition = (5 *10) #mili secondes

spectre = pd.read_csv(fichier_csv)

x = spectre["lambda"].to_numpy()

y1 = spectre["1"].to_numpy()
y2 = spectre["2"].to_numpy()
y3 = spectre["3"].to_numpy()
y4 = spectre["4"].to_numpy()
y5 = spectre["5"].to_numpy()
y6 = spectre["6"].to_numpy()
y7 = spectre["7"].to_numpy()
y8 = spectre["8"].to_numpy()
y9 = spectre["9"].to_numpy()
y10 = spectre["10"].to_numpy()

y = np.sum([y1, y2, y3, y4, y5, y6, y7, y8, y9, y10], axis=0)


plt.figure(figsize=(10, 6))
plt.plot(x, y, label="Spectre total", color="#37379C")
plt.xlabel("Longueur d'onde (nm)", fontsize=20)
plt.ylabel("Compte", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.savefig("spectres_individuels.png", bbox_inches='tight', dpi=600)
plt.show()