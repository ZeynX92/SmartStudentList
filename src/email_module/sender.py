import smtplib
import os
import time
from dotenv import load_dotenv
import mimetypes
from pyfiglet import Figlet
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase


def send_email(recipient: str, key_path):
    print("OK-2")
    sender = "kristall.system@mail.ru"

    load_dotenv()
    password = os.getenv("EMAIL_PASSWORD")
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.starttls()

    try:
        with open('letter.html') as file:
            template_data = file.read()
    except Exception:
        template_data = None

    print("OK-3")

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = "ВсОШ ключи"

        if template_data:
            msg.attach(MIMEText(template_data, "html"))

        filename = os.path.basename(key_path.split('\\')[-1])
        ftype, encoding = mimetypes.guess_type(key_path.split('\\')[-1])
        file_type, subtype = ftype.split("/")
        print("OK-0")
        with open(key_path, "rb") as f:
            file = MIMEBase(file_type, subtype)
            file.set_payload(f.read())
            encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)

        print("OK-1")
        server.sendmail(sender, recipient, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


if __name__ == "__main__":
    font_text = Figlet(font="slant")
    print(font_text.renderText("SEND EMAIL"))
    print(send_email("kristall.system@mail.ru", r'C:\Users\avshe\Desktop\testing\Акимов Александр Павлович.xlsx'))
