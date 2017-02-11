import os
import sys

# Overrides user for local development
USER = ''
if len(sys.argv) > 1 and sys.argv[1] == '--development':
    USER = 'devUser'

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


DEBUG = True
PORT = 3000
