from flask import render_template, Blueprint

calendar = Blueprint('calendar', __name__, template_folder='views')

@calendar.route('/calendar')
def calendar_route():
	options = {}
	return render_template("calendar.html", **options)
