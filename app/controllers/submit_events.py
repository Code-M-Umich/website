from flask import *
import datetime
import hashlib
import smtplib
import random
import string
import jinja2
import math

submit_events = Blueprint('events', __name__, template_folder='views')

PW_FILE_PATH = 'pw.txt'
EMAIL_CODE_M_BOARD = 'code-m-board@umich.edu'
EMAIL_CODE_M_PRES = 'sarthakb@umich.edu'
NAME_CODE_M_PRES = 'Sarty'
TEMPLATE_RES_EMAIL = 'room-reservation-email.txt'
TEMPLATE_SUBMIT_EMAIL = 'event-submission-email.txt'

# jinja2 templates in python
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('views'))

def checkPassword(password):
	m = hashlib.sha512()
	m.update(password)
	hashPass = m.hexdigest()
	
	# get correct hashed pw 
	f = open(PW_FILE_PATH, 'r')
	for line in f:
		key, value = line.split(':', 1)
		if key == 'submit-events':
			correctPw = value
			break

	if hashPass == correctPw:
		return True
	else:
		return False

@submit_events.route('/submit-event', methods=['GET', 'POST'])
def events_route():
	options = {'incorrect':False}

	if request.method == 'POST':
		f = request.form

		# Fail if incorrect password
		if not checkPassword(f['password']):
			return render_template("submit-event.html", incorrect=True)
		
		# convert input times to 12 hour format
		posStartTime12 = datetime.datetime.strptime(f['startTime'], '%H:%M').strftime("%I:%M %p")
		posEndTime12 = datetime.datetime.strptime(f['endTime'], '%H:%M').strftime("%I:%M %p")
		prefStartTime12 = datetime.datetime.strptime(f['prefStartTime'], '%H:%M').strftime("%I:%M %p")

		# calculate preferred ending time
		dur = float(f['eventDuration'])
		min = int((dur * 60)) % 60
		hour = math.floor(dur)
		endTimeObj = datetime.datetime.strptime(f['startTime'], '%H:%M') + datetime.timedelta(hours=hour)
		endTimeObj += datetime.timedelta(minutes=min) #wont work in one line for some reason
		prefEndTime = endTimeObj.strftime("%I:%M %p")

		# create an access code for the event 
		random.seed(datetime.datetime.now())
		code = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
		code = code.lower()

		data = {
			'hostEmail' : f['hostEmail'],
			'eventName' : f['eventName'],
			'dateOfEvent' : f['eventDate'],
			'possibleStartTime' : f['startTime'],
			'possibleStartTime12' : posStartTime12,
			'possibleEndTime' :f['endTime'],
			'possibleEndTime12' : posEndTime12,
			'prefStartTime' : f['prefStartTime'],
			'prefStartTime12' : prefStartTime12,
			'building' : f['building'],
			'room' : f['room'],
			'eventDuration' : f['eventDuration'],
			'shortDesc' : f['desc'],
			'fullDesc' : f['fullDesc'],
			'eventType' : f['eventType'],
			'accessCode' : code
		}
	
		# TODO: sanitize input
		######
		# TODO: insert into database

		recipients = [data['hostEmail']]
		if f['cohostEmail'] is not None:
			data['cohostEmail'] = f['cohostEmail']
			recipients.append(data['cohostEmail'])
		
		if f['isReserved'] == 'no':
			reserveRoom(f, prefStartTime12, prefEndTime, posStartTime12, posEndTime12)
			data['isReserved'] = False
			data['roomSize'] = f['roomSize']
		else:
			data['isReserved'] = True

		
		# form and send email to hosts / board
		template = ENV.get_template(TEMPLATE_SUBMIT_EMAIL)
		message = template.render(**data)

		sendEmail(message, EMAIL_CODE_M_BOARD, recipients)
		

	
	return render_template("submit-event.html", **options)



# Drafts email for reserving room, currently only valid for north campus
def reserveRoom(f, startTime, endTime, possibleStartTime, possibleEndTime):

		person = NAME_CODE_M_PRES
		recipientEmail = EMAIL_CODE_M_PRES

		# gather email data
		data = {
			'recipientName' : person,
			'recipientEmail' : recipientEmail,
			'senderEmail' : EMAIL_CODE_M_BOARD,
			'building' : f['building'],
			'roomSize' : f['roomSize'],
			'room' : f['room'],
			'startTime' : startTime,
			'endTime' : endTime,
			'startRange' : possibleStartTime,
			'endRange' : possibleEndTime,
			'duration' : f['eventDuration']
		}


		# read template 
		template = ENV.get_template(TEMPLATE_RES_EMAIL)
		message = template.render(**data)

		return sendEmail(message, EMAIL_CODE_M_BOARD, recipientEmail)


# sends email, returns false if failed
def sendEmail(message, sender, receiver):

	return message
	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receiver, message)
		return True
	except SMTPException:
		return False