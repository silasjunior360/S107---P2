
import os
import smtplib
from email.message import EmailMessage

def send_email():
    
    sender_email = os.getenv('MAIL_SENDER')
    sender_password = os.getenv('MAIL_PASSWORD')
    recipient_email = os.getenv('MAIL_RECIPIENT')

    if not all([sender_email, sender_password, recipient_email]):
        print("Erro: As variáveis de ambiente MAIL_SENDER, MAIL_PASSWORD, e MAIL_RECIPIENT devem ser definidas.")
        exit(1)

    msg = EmailMessage()
    msg['Subject'] = "Notificação de Execução do Pipeline de CI/CD"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content("O pipeline de CI/CD para o projeto de S107 foi executado com sucesso!")

    try:
        print(f"Tentando enviar e-mail de {sender_email} para {recipient_email}...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar o e-mail: {e}")
        exit(1)

if __name__ == "__main__":
    send_email()
