import os

DEBUG=False
SQLALCHEMY_TRACK_MODIFICATIONS=False

MAIL_SERVER='email-smtp.us-east-1.amazonaws.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=os.environ["MAIL_USERNAME"]
MAIL_PASSWORD=os.environ["MAIL_PASSWORD"]
