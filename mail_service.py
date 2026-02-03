import csv
import smtplib
import ssl
import time
from email.message import EmailMessage

EMAIL_ADDRESS = "abc@gmail.com"
APP_PASSWORD = "aaaa bbbb cccc dddd"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL
context = ssl.create_default_context()

def create_message(to_email):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = "Anfrage Ersttermin – gesetzlich versicherte/r Neupatient/in"

    body = """Sehr geehrtes Praxisteam,

ich möchte höflich anfragen, ob Sie aktuell neue Patient*innen mit gesetzlicher Krankenversicherung aufnehmen oder ob die Möglichkeit besteht, auf eine Warteliste gesetzt zu werden.

Kurz zu mir:
Mein Name ist [], ich bin [] Jahre alt und [Beschäftigung].

Seit längerer Zeit bestehen bei mir deutliche [Symptome].
Da die Symptome mein/e [Beschäftigung/Leben] zunehmend beeinträchtigen, wünsche ich mir eine [xxx-ärzliche] Einschätzung. Auch eine diagnostische Abklärung ohne direkte Therapieoption wäre für mich bereits sehr hilfreich.

Meine zeitliche Verfügbarkeit für Termine ist:
[Tage/Uhrzeiten].

Falls aktuell keine Kapazitäten bestehen, wäre ich Ihnen auch für Hinweise auf Kolleg*innen dankbar.

Über eine kurze Rückmeldung zu Terminmöglichkeiten oder Wartezeiten würde ich mich sehr freuen.

Mit freundlichen Grüßen  
[Name]
[Nummer]
"""
    msg.set_content(body)
    return msg

# Open a single SMTP_SSL connection
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
    server.login(EMAIL_ADDRESS, APP_PASSWORD)

    # Read the CSV
    with open("psychiater.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # <-- important if CSV uses semicolons, change as needed or remove (default is comma)
        print("CSV headers:", reader.fieldnames)  # optional: verify headers

        for row in reader:
            try:
                email = row["Email"].strip()  # Use exact column name in the csv (case-sensitive)
                if email:  # skip empty emails
                    msg = create_message(email)
                    server.send_message(msg)
                    print(f"✅ Sent to {email}")
                    time.sleep(20)  # polite delay to avoid being marked as spam
            except Exception as e:
                print(f"❌ Failed for {row.get('Email', 'UNKNOWN')}: {e}")
