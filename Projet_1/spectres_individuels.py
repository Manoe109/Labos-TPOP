import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

dossier_script = os.path.dirname(os.path.abspath(__file__))
fichier_csv = os.path.join(dossier_script, "obj1.csv")
duree_exposition = 5 #mili secondes

spectre = pd.read_csv(fichier_csv)

x = spectre["lambda"].to_numpy()

y1 = spectre["alex_rouge"].to_numpy()
y2 = spectre["alex_bleu"].to_numpy()
y3 = spectre["alex_blanc"].to_numpy()
y4 = spectre["mathilde"].to_numpy()
y5 = spectre["a_c"].to_numpy()

y = np.sum([y1, y2, y3, y4, y5], axis=0)


plt.figure(figsize=(10, 6))
plt.plot(x, y, label="Spectre total", color="#37379C")
plt.xlabel("Longueur d'onde (nm)")
plt.ylabel("Comptes")
plt.show()