from flask import render_template, Blueprint

events = Blueprint('events', __name__, template_folder='views')

@events.route('/SubmitEvent')
def events_route():
	options = {}
	return render_template("events.html", **options)
