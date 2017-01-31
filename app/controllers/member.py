from flask import render_template, Blueprint
from database import openDBConnection, closeDBConnection, DBCommit
member = Blueprint('member', __name__, template_folder='views')

def get_members(uniqname, eventID):
	cur = openDBConnection()
	query = "INSERT INTO attendance (uniqname, event) " \
			"VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
	cur.execute(query)
	DBCommit()
	closeDBConnection()

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
	entries = cur.fetchall()
	print entries
	points = 0	
	closeDBConnection()	
	return points

def get_admin(uniqname):
	cur = openDBConnection()
	query = "SELECT admin from users " \
			"WHERE uniqname = \"%s\";" % uniqname
	cur.execute(query)
	entries = cur.fetchall()
	print entries
	if len(entries):
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

@member.route('/member')
def member_route():
	options = {}
	return render_template("member.html", **options)
