import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def enviarCorreo(destino, asunto, cuerpo, pdf=False, pdfName="factura"):
    # Crea el mensaje
    message = MIMEMultipart()
    message["From"] = "titoscarly177@gmail.com"
    message["To"] = destino
    message["Subject"] = asunto

    # Agrega el cuerpo del mensaje en UTF-8
    message.attach(MIMEText(cuerpo, "plain", "utf-8"))

    # Agrega el PDF como adjunto
    if pdf:
        pdf_attachment = MIMEApplication(pdf, _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition", "attachment", filename=f"{pdfName}.pdf"
        )
        message.attach(pdf_attachment)

    # Envía el correo
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.ehlo()
        server.login(message["From"], "qdxz vyzb bgrn laap")
        server.sendmail(message["From"], destino, message.as_string())
