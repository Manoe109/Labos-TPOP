// Broche de lecture
const int sensorPin = A0;

// Paramètres du circuit
const float R_load       = 10000.0; // Résistance de charge en Ohms
const float V_ref        = 5.0;     // Tension de référence Arduino
const float responsivity = 0.325;    // Responsivité DET100A2 (A/W)     selon la longueur d'onde, à changer

void setup() {
  Serial.begin(9600);
  Serial.println("Début de la lecture du capteur de courant.");
}

void loop() {
  int rawValue = analogRead(sensorPin);

  // 1. Tension (V)
  float voltage = (rawValue / 1023.0) * V_ref;

  // 2. Courant (A)
  float courant = voltage / R_load;

  // 3. Puissance lumineuse estimée (W)
  float puissance = courant / responsivity;

  Serial.print("Tension: ");
  Serial.print(voltage, 4);
  Serial.print(" V | Courant: ");
  Serial.print(courant * 1e6, 2);   // En µA
  Serial.print(" uA | Puissance: ");
  Serial.print(puissance * 1e6, 2); // En µW
  Serial.println(" uW");

  delay(500);
}