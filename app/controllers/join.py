from flask import render_template, Blueprint

join = Blueprint('join', __name__, template_folder='views')

@join.route('/join')
def join_route():
	options = {}
	return render_template("join.html", **options)
