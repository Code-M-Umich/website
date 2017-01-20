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
MYSQL_HOST = ""
MYSQL_PORT = 3306
MYSQL_USER = "labwatch"
MYSQL_PASSWORD = "rpbcbcbdargfk74"

if ENV == 'dev':
    DEBUG = True
    PORT = 5000
elif ENV == 'prod':
    DEBUG = False
    PORT = 5000

elif ENV == 'local':
    DEBUG = True
    PORT = 5000

else:
    DEBUG = True
    PORT = 5000
