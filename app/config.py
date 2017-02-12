import os
import argparse


# Create and handle command line arguments
parser = argparse.ArgumentParser(description='Website for Code-M')
parser.add_argument('-d', '--development', 
					action="store_true", # act like a flag
                    help='a flag for indicating the app will run for local development')
parser.add_argument('-u', default='devUser', type=str,
                    help='uniqname for the session (who you are signed in as)')
parser.add_argument('-s', '--socket', default=None, type=str,
                    help='Fix for database not working locally. Provide the filepath given by \
                    running the command \'mysqladmin | grep socket\'')
args = parser.parse_args()

# If app is run with development, fake a logged in user
USER = ''
if args.development and args.u:
    USER = args.u

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
