# Fichier qui montre comment lire le courant d'un capteur DET100A2

# Longueur d'onde du laser: X nm
# Responsivité typique du DET100A2: X A/W

# Schéma de connexion (exemple trouvé):

#       (Photodiode &
#       Internal Bias)
#
#       [BNC Central] (Signal +) ----------o-----------o--> Vers ARDUINO Broche A0
#                                         |           |
#                                         |           |
#                                         |           |
#                                       [ R_Load]   [ C_1 ] (Optionnel)
#                                       [ 10 kOhm]  [0.1 uF]
#                                         |           |
#                                         |           |
#                                         |           |
#       [BNC Blindage] (GND) --------------o-----------o--> Vers ARDUINO Broche GND

import serial
import csv
import time
import sys
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIGURATION 
# ─────────────────────────────────────────
PORT     = "COM3"       # à changer selon l'ordi
BAUDRATE = 9600
DURATION = 30           # Durée d'enregistrement en secondes
OUTPUT   = f"mesures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
# ─────────────────────────────────────────

def parse_line(line: str) -> dict | None:
    """
    Parse une ligne du type:
    'Tension: 0.0123 V | Courant: 1.23 uA | Puissance: 2.74 uW'
    Retourne un dict ou None si la ligne est invalide.
    """
    try:
        parts = line.split("|")
        tension   = float(parts[0].split(":")[1].replace("V", "").strip())
        courant   = float(parts[1].split(":")[1].replace("uA", "").strip())
        puissance = float(parts[2].split(":")[1].replace("uW", "").strip())
        return {"tension_V": tension, "courant_uA": courant, "puissance_uW": puissance}
    except (IndexError, ValueError):
        return None  # Ligne non parseable (ex: message de démarrage)


def main():
    print(f"Connexion sur {PORT} à {BAUDRATE} bauds...")

    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    except serial.SerialException as e:
        print(f"Erreur : impossible d'ouvrir le port — {e}")
        sys.exit(1)

    time.sleep(2)  # Attendre la réinitialisation de l'Arduino
    ser.reset_input_buffer()

    print(f"Enregistrement pendant {DURATION} secondes → {OUTPUT}")
    print("─" * 50)

    row_count  = 0
    start_time = time.time()

    with open(OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp_s", "tension_V", "courant_uA", "puissance_uW"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while (elapsed := time.time() - start_time) < DURATION:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue

            data = parse_line(raw)
            if data:
                data["timestamp_s"] = round(elapsed, 3)
                writer.writerow(data)
                row_count += 1

                # Affichage en temps réel dans le terminal
                remaining = DURATION - elapsed
                print(f"[{elapsed:6.2f}s | {remaining:.1f}s restantes]  "
                      f"{data['tension_V']:.4f} V | "
                      f"{data['courant_uA']:.2f} uA | "
                      f"{data['puissance_uW']:.2f} uW")

    ser.close()
    print("─" * 50)
    print(f" Terminé — {row_count} lignes enregistrées dans '{OUTPUT}'")


if __name__ == "__main__":
    main()