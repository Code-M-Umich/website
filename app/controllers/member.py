from flask import render_template, Blueprint

member = Blueprint('member', __name__, template_folder='views')

def get_points(uniqname):
	cur = mysql.connection.cursor()
	query = "SELECT SUM(events.points) from events " \
		"JOIN attendance ON events.eventid = attendance.event " \
		"WHERE attendance.uniqname = \"%s\";" % uniqname
	cur.execute(query)
	entries = cur.fetchall()
	print entries
	points = 0		
	return points

@member.route('/member')
def member_route():
	options = {}
	return render_template("member.html", **options)
