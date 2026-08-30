import os
from flask_mail import Mail

mail = Mail()

def configure_mail(app):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("EMAIL_ADDRESS")
    app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_ADDRESS")

    mail.init_app(app)