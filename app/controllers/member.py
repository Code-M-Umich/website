from flask import render_template, Blueprint

member = Blueprint('member', __name__, template_folder='views')

def get_members(uniqname, eventID):
	cur = mysql.connection.cursor()
	query = "INSERT INTO codeM.attendance (uniqname, event) " \
			"VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
	cur.execute(query)
	mysql.connection.commit()
	cur.close()

def add_attendence(uniqname, eventID):
	cur = mysql.connection.cursor()
	query = "INSERT INTO codeM.attendance (uniqname, event) " \
			"VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
	cur.execute(query)
	mysql.connection.commit()
	cur.close()

def get_points(uniqname):
	cur = mysql.connection.cursor()
	query = "SELECT SUM(events.points) from events " \
		"JOIN attendance ON events.eventid = attendance.event " \
		"WHERE attendance.uniqname = \"%s\";" % uniqname
	cur.execute(query)
	entries = cur.fetchall()
	print entries
	points = 0	
	cur.close()	
	return points

def get_admin(uniqname):
	cur = mysql.connection.cursor()
	query = "SELECT admin from users " \
			"WHERE uniqname = \"%s\";" % uniqname
	cur.execute(query)
	entries = cur.fetchall()
	print entries
	if len(entries):
		cur.close()
		#check whether received true or false

		return True
	else len(entries):
		query = "INSERT INTO codem.users (uniqname) " \
				"VALUES (\"%s\")" % (uniqname)
		cur.execute(query)
		mysql.connection.commit()
		cur.close()
		#not admin by default
		return False
	
	return True

@member.route('/member')
def member_route():
	options = {}
	return render_template("member.html", **options)
