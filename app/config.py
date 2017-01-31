import os

ENV = os.environ.get('ENVIRONMENT', 'dev')
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'YELLOWSUBMARINE'

# Email set-up
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'test@gmail.com'
MAIL_PASSWORD = 'testing'

#database stuff
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "codem"
MYSQL_PASSWORD = "YELLOWSUBMARINE"
MYSQL_DB = "codem"

DEBUG = True
PORT = 3000
