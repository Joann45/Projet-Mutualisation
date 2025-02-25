#!/bin/bash

echo "📧 Test de connexion SMTP avec Gmail..."

# Définir les variables
EMAIL="stageflow45@gmail.com"
PASSWORD="TON_MOT_DE_PASSE_APPLICATION"  # Remplace par ton mot de passe d'application

# Exécuter un script Python pour tester SMTP
python3 <<EOF
import smtplib

EMAIL = "$EMAIL"
PASSWORD = "$PASSWORD"

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASSWORD)
    print("✅ Connexion réussie à Gmail SMTP")
    server.quit()
except Exception as e:
    print("❌ Erreur de connexion SMTP :", e)
EOF

