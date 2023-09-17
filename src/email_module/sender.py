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
    sender = "system.kristall@mail.ru"

    load_dotenv()
    password = os.getenv("EMAIL_PASSWORD")
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.starttls()

    server.login(sender, password)
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "ВсОШ ключи"

    msg.attach(MIMEText(
        'Приветствую! Меня зовут Аврора, отвечаю за документы в экосистеме Kristall\nДля тебя у меня есть файл с твоими ключами для участия во Всероссийской Олимпиаде Школьников\n\n\nДанное письмо было сгенерировано подсистемой "Аквамарин" и не требует ответа'))

    filename = os.path.basename(key_path.split('\\')[-1])
    ftype, encoding = mimetypes.guess_type(key_path.split('\\')[-1])
    file_type, subtype = ftype.split("/")

    with open(key_path, "rb") as f:
        file = MIMEBase(file_type, subtype)
        file.set_payload(f.read())
        encoders.encode_base64(file)

        file.add_header('content-disposition', 'attachment', filename=filename)
        msg.attach(file)

    server.sendmail(sender, recipient, msg.as_string())


if __name__ == "__main__":
    font_text = Figlet(font="slant")
    print(font_text.renderText("SEND EMAIL"))
    print(send_email("kristall.system@mail.ru", r'C:\Users\avshe\Desktop\testing\Акимов Александр Павлович.xlsx'))








































































































































































