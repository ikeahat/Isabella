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

# comments may be outdated, shit got reworked and comments got ignored somewhat XD

def read_csv(): # read psychiater.csv, put data into dictionaries with fieldnames as keys.
    all_entries = []
    with open("psychiater.csv", newline="", encoding="ANSI") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # <-- important if CSV uses semicolons, change as needed or remove (default is comma)
        for row in reader:
            entry = {}
            for field in reader.fieldnames:
                entry[field] = row[field].strip()
            all_entries.append(entry)
    return all_entries

def get_emails_from_entries(e): # get a list of all email strings from the output of read_csv()
    l = []
    for entry in e:
        if entry["Email"]:
            l.append(entry["Email"])
    return l

def execute(emails): # send all EMails.
    # Open a single SMTP_SSL connection
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        for email in emails:
            try:
                if email:  # skip empty emails
                    msg = create_message(email)
                    server.send_message(msg)
                    print(f"successfully sent to {email}")
                    time.sleep(20)  # polite delay to avoid being marked as spam
            except Exception as e:
                print(f"failed for {email}: {e}")


def run_program():  # run ts x3
    entries = read_csv()
    mails = get_emails_from_entries(entries)

    for entry in entries:
        if not entry["Email"]:
            continue
        print(f"{entry['Email']} | {entry['Distance']} | {entry['Name']}")
    
    print(f"\n\n{len(mails)}/{len(entries)} addresses found ^")
    x = ""
    print()
    while x != "y":
        x = input("send email to ALL OF THEM? (y/n): ")
        if x == "n":
            quit()
    print("sending...")
    execute(mails)
    
run_program()



