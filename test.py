import smtpd, ssl, smtplib, getpass


def send_email():
    #  salefinder.NED@gmail.com
    port = 465
    password = 'haruc4h9'  # todo getpass.getpass()
    sender_email = "salefinder.ned@gmail.com"
    reciever_email = "ericdong97@gmail.com"
    smtp_server = 'smtp.gmail.com'
    message = "hello"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)


send_email()