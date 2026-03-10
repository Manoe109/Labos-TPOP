import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

#aller chercher fichier
dossier_script = os.path.dirname(os.path.abspath(__file__))


#spectre 1 lampe alex bleu
fichier_csv_atbleu = os.path.join(dossier_script, "spectre_atbleu.csv")
spectre = pd.read_csv(fichier_csv_atbleu)

y1_atbleu = spectre["alex_rouge"].to_numpy()
y2_atbleu = spectre["alex_bleu"].to_numpy()
y3_atbleu = spectre["alex_blanc"].to_numpy()
y4_atbleu = spectre["mathilde"].to_numpy()
y5_atbleu = spectre["a_c"].to_numpy()

y_atbleu = np.sum([y1_atbleu, y2_atbleu, y3_atbleu, y4_atbleu, y5_atbleu], axis=0)


#spectre 2 lampe alex rouge
fichier_csv_atrouge = os.path.join(dossier_script, "spectre_atrouge.csv")
spectre = pd.read_csv(fichier_csv_atrouge)

y1_atrouge = spectre["alex_rouge"].to_numpy()
y2_atrouge = spectre["alex_bleu"].to_numpy()
y3_atrouge = spectre["alex_blanc"].to_numpy()
y4_atrouge = spectre["mathilde"].to_numpy()
y5_atrouge = spectre["a_c"].to_numpy()

y_atrouge = np.sum([y1_atrouge, y2_atrouge, y3_atrouge, y4_atrouge, y5_atrouge], axis=0)


#spectre 3 lampe alex blanc
fichier_csv_atblanc = os.path.join(dossier_script, "spectre_atblanc.csv")
spectre = pd.read_csv(fichier_csv_atblanc)

y1_atblanc = spectre["alex_rouge"].to_numpy()
y2_atblanc = spectre["alex_bleu"].to_numpy()
y3_atblanc = spectre["alex_blanc"].to_numpy()
y4_atblanc = spectre["mathilde"].to_numpy()
y5_atblanc = spectre["a_c"].to_numpy()

y_atblanc = np.sum([y1_atblanc, y2_atblanc, y3_atblanc, y4_atblanc, y5_atblanc], axis=0)


#spectre 4 lampe mathilde
fichier_csv_mn = os.path.join(dossier_script, "spectre_mn.csv")
spectre = pd.read_csv(fichier_csv_mn)

y1_mn = spectre["alex_rouge"].to_numpy()
y2_mn = spectre["alex_bleu"].to_numpy()
y3_mn = spectre["alex_blanc"].to_numpy()
y4_mn = spectre["mathilde"].to_numpy()
y5_mn = spectre["a_c"].to_numpy()

y_mn = np.sum([y1_mn, y2_mn, y3_mn, y4_mn, y5_mn], axis=0)


#spectre 5 lampe marie-eve
fichier_csv_men = os.path.join(dossier_script, "spectre_men.csv")
spectre = pd.read_csv(fichier_csv_men)

y1_men = spectre["alex_rouge"].to_numpy()
y2_men = spectre["alex_bleu"].to_numpy()
y3_men = spectre["alex_blanc"].to_numpy()
y4_men = spectre["mathilde"].to_numpy()
y5_men = spectre["a_c"].to_numpy()

y_men = np.sum([y1_men, y2_men, y3_men, y4_men, y5_men], axis=0)


#spectre 6 lampe annie-claude
fichier_csv_ac = os.path.join(dossier_script, "spectre_ac.csv")
spectre = pd.read_csv(fichier_csv_ac)

y1_ac = spectre["alex_rouge"].to_numpy()
y2_ac = spectre["alex_bleu"].to_numpy()
y3_ac = spectre["alex_blanc"].to_numpy()
y4_ac = spectre["mathilde"].to_numpy()
y5_ac = spectre["a_c"].to_numpy()

y_ac = np.sum([y1_ac, y2_ac, y3_ac, y4_ac, y5_ac], axis=0)


#graphique des spectres
x = spectre["lambda"].to_numpy()

plt.figure(figsize=(10, 6))
plt.plot(x, y_atbleu, label="Spectre lampe Alex bleu", color="#040470")
plt.plot(x, y_atrouge, label="Spectre lampe Alex rouge", color="#841616")
plt.plot(x, y_atblanc, label="Spectre lampe Alex blanc", color="#007980")
plt.plot(x, y_mn, label="Spectre lampe Mathilde", color='#008000')
plt.plot(x, y_men, label="Spectre lampe Marie-Eve", color='#FFA500')
plt.plot(x, y_ac, label="Spectre lampe Annie-Claude", color='#800080')
plt.xlabel("Longueur d'onde (nm)")
plt.ylabel("Compte")
plt.legend()
plt.show()