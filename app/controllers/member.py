from flask import render_template, Blueprint
from database import openDBConnection, closeDBConnection, DBCommit
from includes import randomCompliment

member = Blueprint('member', __name__, template_folder='views')

def get_members(uniqname, eventID):
	cur = openDBConnection()
	query = "INSERT INTO attendance (uniqname, event) " \
			"VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
	cur.execute(query)
	DBCommit()
	closeDBConnection()

# returns all the peope who attended an event 
def get_event_attendance(eventID):
	cur = openDBConnection()
	query = "SELECT uniqname FROM codeM.attendance WHERE eventID=\"%d\";" % eventID
	cur.execute(query)
	entries = cur.fetchall()
	closeDBConnection()
	return entries

def add_attendence(uniqname, eventID):
	cur = openDBConnection()
	query = "INSERT INTO attendance (uniqname, event) " \
			"VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
	cur.execute(query)
	DBCommit()
	closeDBConnection()

def get_points(uniqname):
	cur = openDBConnection()
	query = "SELECT SUM(events.points) from events " \
		"JOIN attendance ON events.eventid = attendance.event " \
		"WHERE attendance.uniqname = \"%s\";" % uniqname
	cur.execute(query)
	entries = cur.fetchone()
	print entries
<<<<<<< HEAD
	points = 0	
	closeDBConnection()	
=======
	points = entries['points']
	cur.close()	
>>>>>>> d47ad4b152576c0d273c771aaf7a1dbc810417f0
	return points

# Returns true if a given user is an admin
def get_admin(uniqname):
	cur = openDBConnection()
	query = "SELECT admin from users " \
			"WHERE uniqname = \"%s\" LIMIT 1" % uniqname
	cur.execute(query)
	entries = cur.fetchall()
	print entries
	if len(entries):
<<<<<<< HEAD
		closeDBConnection()
		#check whether received true or false

		return True
	else:
		query = "INSERT INTO users (uniqname) " \
				"VALUES (\"%s\")" % (uniqname)
		cur.execute(query)
		DBCommit()
		closeDBConnection()
		#not admin by default
		return False
	
	return True
=======
		cur.close()
		return True
	return False

# Adds user to the database once they visit the memebers page
def add_user(uniqname):
	query = "INSERT INTO codem.users (uniqname) " \
				"VALUES (\"%s\")" % (uniqname)
	cur.execute(query)
	mysql.connection.commit()
	cur.close()

# TODO: def add_admin(uniqname):
>>>>>>> d47ad4b152576c0d273c771aaf7a1dbc810417f0

# Checks to see if the user entered accessCode is correct for a given event
def validateAttendance(uniqname, userEnteredCode, eventID):
	cur = mysql.connection.cursor()
	query = "SELECT accessCode FROM events WHERE eventID=\"%d\" AND open=1 LIMIT 1" % (eventID)
	cur.execute(query)
	accessCode = cur.fetchone()
	cur.close()
	if userEnteredCode == accessCode:
		add_attendence(uniqname, eventID)
		return True
	else:
		 return False

# returns all the details about an event
def get_event(eventid):
	cur = mysql.connection.cursor()
	query = "SELECT * FROM events WHERE eventID=\"%d\";" % (eventID)
	cur.execute(query)
	entry = cur.fetchone()
	cur.close()
	return entry

# Returns all the currently open events
def get_open_events():
	cur = mysql.connection.cursor()
	query = "SELECT * FROM events WHERE open=1"
	cur.execute(query)
	entries = cur.fetchall()
	cur.close()
	return entries

@member.route('/member', methods=['GET', 'POST'])
def member_route():
	options = {}
	user = request.environ['REMOTE_USER'] #should always be valid with cosign
	isAuth = False
	didSubmit = False

	# Handle event code submission
	if request.method == 'POST' and request.form['eventCode']:
		didSubmit = True
		f = request.form
		eventID= f['eventID']
		if validateAttendance(user, f['eventCode'], eventID):
			isAuth = True
			event = get_event(eventID)
			options['authedEventName'] = event['name']
		


	options = {
		'user' : user,
		'event' : get_open_events(),
		'didSubmitCode' : didSubmit,
		'isAuth' : isAuth,
		'points' : get_points(user),
		'compliment' : randomCompliment()
	} 

	return render_template("member.html", **options)
