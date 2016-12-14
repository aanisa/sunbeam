import os

DEBUG=False
SQLALCHEMY_TRACK_MODIFICATIONS=False

SURVEY_MONKEY_OAUTH_TOKEN=os.environ['SURVEY_MONKEY_OAUTH_TOKEN']
SURVEY_MONKEY_SURVEY_ID='111419034'
SURVEY_MONKEY_COLLECTOR_ID='FQDVNM3'
SURVEY_MONKEY_WHICH_SCHOOLS_QUESTION_ID='69085210'
SURVEY_MONKEY_EMAIL_QUESTION_IDS=['69078871', '69078871']

MAIL_SERVER='email-smtp.us-east-1.amazonaws.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=os.environ["MAIL_USERNAME"]
MAIL_PASSWORD=os.environ["MAIL_PASSWORD"]
