import smtplib
import os

# Recupera le variabili d'ambiente impostate su Railway
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

print("Sto testando la connessione SMTP...")

try:
    # Connessione SSL a Gmail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SMTP_USER, SMTP_PASSWORD)
    print("✅ Connessione SMTP riuscita!")
    server.quit()
except Exception as e:
    print("❌ Errore SMTP:", e)
