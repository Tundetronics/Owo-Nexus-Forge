import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('The Sovereign Forge is online. Email delivery logic is verified.')
msg['Subject'] = 'Owo-Nexus: System Connectivity Confirmed'
msg['From'] = 'tundetronics@gmail.com'
msg['To'] = 'tundetronics@gmail.com'

try:
    print("Initiating Sovereign Handshake with Gmail...")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # This will ask you for the password when you run the script
        password = input('Paste your 16-char App Password (NO SPACES): ')
        smtp.login('tundetronics@gmail.com', password)
        smtp.send_message(msg)
    print('\nSUCCESS: Email sent! Your secrets are valid. The Forge is armed.')
except Exception as e:
    print(f'\nFAILURE: {e}')