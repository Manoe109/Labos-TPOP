import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

#lampe 1 : MN
#lampe 2 : MEN
#lampe 3 : AC
#lampe 4 : AT

#aller chercher fichier
dossier_script = os.path.dirname(os.path.abspath(__file__))

lampe_1 ="#B0B0B0"
lampe_2 = "#575757"
lampe_3 = "#3E3E3E"
lampe_4 = "#000000"

#spectre 1 lampe alex bleu
fichier_csv_atbleu = os.path.join(dossier_script, "spectre_at_bleu.csv")
spectre_at_bleu = pd.read_csv(fichier_csv_atbleu)

y1_atbleu = spectre_at_bleu["1"].to_numpy()
y2_atbleu = spectre_at_bleu["2"].to_numpy()
y3_atbleu = spectre_at_bleu["3"].to_numpy()
y4_atbleu = spectre_at_bleu["4"].to_numpy()
y5_atbleu = spectre_at_bleu["5"].to_numpy()
y6_atbleu = spectre_at_bleu["6"].to_numpy()
y7_atbleu = spectre_at_bleu["7"].to_numpy()
y8_atbleu = spectre_at_bleu["8"].to_numpy()
y9_atbleu = spectre_at_bleu["9"].to_numpy()
y10_atbleu = spectre_at_bleu["10"].to_numpy()

y_atbleu = np.sum([y1_atbleu, y2_atbleu, y3_atbleu, y4_atbleu, y5_atbleu, y6_atbleu, y7_atbleu, y8_atbleu, y9_atbleu, y10_atbleu], axis=0)


#spectre 2 lampe alex rouge
fichier_csv_atrouge = os.path.join(dossier_script, "spectre_at_rouge.csv")
spectre_at_rouge = pd.read_csv(fichier_csv_atrouge)

y1_atrouge = spectre_at_rouge["1"].to_numpy()
y2_atrouge = spectre_at_rouge["2"].to_numpy()
y3_atrouge = spectre_at_rouge["3"].to_numpy()
y4_atrouge = spectre_at_rouge["4"].to_numpy()
y5_atrouge = spectre_at_rouge["5"].to_numpy()
y6_atrouge = spectre_at_rouge["6"].to_numpy()
y7_atrouge = spectre_at_rouge["7"].to_numpy()
y8_atrouge = spectre_at_rouge["8"].to_numpy()
y9_atrouge = spectre_at_rouge["9"].to_numpy()
y10_atrouge = spectre_at_rouge["10"].to_numpy()


y_atrouge = np.sum([y1_atrouge, y2_atrouge, y3_atrouge, y4_atrouge, y5_atrouge, y6_atrouge, y7_atrouge, y8_atrouge, y9_atrouge, y10_atrouge], axis=0)


#spectre 3 lampe alex blanc
fichier_csv_atblanc = os.path.join(dossier_script, "spectre_at_blanc.csv")
spectre_at_blanc = pd.read_csv(fichier_csv_atblanc)

y1_atblanc = spectre_at_blanc["1"].to_numpy()
y2_atblanc = spectre_at_blanc["2"].to_numpy()
y3_atblanc = spectre_at_blanc["3"].to_numpy()
y4_atblanc = spectre_at_blanc["4"].to_numpy()
y5_atblanc = spectre_at_blanc["5"].to_numpy()
y6_atblanc = spectre_at_blanc["6"].to_numpy()
y7_atblanc = spectre_at_blanc["7"].to_numpy()   
y8_atblanc = spectre_at_blanc["8"].to_numpy()
y9_atblanc = spectre_at_blanc["9"].to_numpy()
y10_atblanc = spectre_at_blanc["10"].to_numpy()

y_atblanc = np.sum([y1_atblanc, y2_atblanc, y3_atblanc, y4_atblanc, y5_atblanc, y6_atblanc, y7_atblanc, y8_atblanc, y9_atblanc, y10_atblanc], axis=0)


#spectre 4 lampe mathilde
fichier_csv_mn = os.path.join(dossier_script, "spectre_mn.csv")
spectre_mn = pd.read_csv(fichier_csv_mn)

y1_mn = spectre_mn["1"].to_numpy()
y2_mn = spectre_mn["2"].to_numpy()
y3_mn = spectre_mn["3"].to_numpy()
y4_mn = spectre_mn["4"].to_numpy()
y5_mn = spectre_mn["5"].to_numpy()
y6_mn = spectre_mn["6"].to_numpy()
y7_mn = spectre_mn["7"].to_numpy()
y8_mn = spectre_mn["8"].to_numpy()
y9_mn = spectre_mn["9"].to_numpy()
y10_mn = spectre_mn["10"].to_numpy()    

y_mn = np.sum([y1_mn, y2_mn, y3_mn, y4_mn, y5_mn, y6_mn, y7_mn, y8_mn, y9_mn, y10_mn], axis=0)


#spectre 5 lampe marie-eve
fichier_csv_men = os.path.join(dossier_script, "spectre_men.csv")
spectre_men = pd.read_csv(fichier_csv_men)

y1_men = spectre_men["1"].to_numpy()
y2_men = spectre_men["2"].to_numpy()
y3_men = spectre_men["3"].to_numpy()
y4_men = spectre_men["4"].to_numpy()
y5_men = spectre_men["5"].to_numpy()
y6_men = spectre_men["6"].to_numpy()
y7_men = spectre_men["7"].to_numpy()
y8_men = spectre_men["8"].to_numpy()
y9_men = spectre_men["9"].to_numpy()
y10_men = spectre_men["10"].to_numpy()

y_men = np.sum([y1_men, y2_men, y3_men, y4_men, y5_men, y6_men, y7_men, y8_men, y9_men, y10_men], axis=0)


#spectre 6 lampe annie-claude
fichier_csv_ac = os.path.join(dossier_script, "spectre_ac.csv")
spectre_ac = pd.read_csv(fichier_csv_ac)

y1_ac = spectre_ac["1"].to_numpy()
y2_ac = spectre_ac["2"].to_numpy()
y3_ac = spectre_ac["3"].to_numpy()
y4_ac = spectre_ac["4"].to_numpy()
y5_ac = spectre_ac["5"].to_numpy()
y6_ac = spectre_ac["6"].to_numpy()
y7_ac = spectre_ac["7"].to_numpy()
y8_ac = spectre_ac["8"].to_numpy()
y9_ac = spectre_ac["9"].to_numpy()
y10_ac = spectre_ac["10"].to_numpy()

y_ac = np.sum([y1_ac, y2_ac, y3_ac, y4_ac, y5_ac, y6_ac, y7_ac, y8_ac, y9_ac, y10_ac], axis=0)


#graphique des spectres
x = spectre_men["lambda"].to_numpy()

plt.figure(figsize=(10, 6))
plt.plot(x, y_mn, label="Lampe 1", linestyle='-', color=lampe_1)
#plt.plot(x, y_men, label="Lampe 2", linestyle='-', color=lampe_2)
plt.plot(x, y_ac, label="Lampe 3", linestyle='-', color=lampe_3)
#plt.plot(x, y_atbleu, label="Lampe 4", linestyle='-', color=lampe_4)
plt.plot(x, y_atblanc, label="Lampe 4.2", linestyle='-', color="#09DEE9")
#plt.plot(x, y_atrouge, label="Lampe 4.3", linestyle='-', color="#AC4F4F")
plt.xlabel("Longueur d'onde (nm)", fontsize=20)
plt.ylabel("Compte", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
plt.savefig("spectres_comparaison_2.png", bbox_inches='tight', dpi=600)
plt.show()