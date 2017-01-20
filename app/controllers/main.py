from flask import render_template, Blueprint

main = Blueprint('main', __name__, template_folder='views')

@main.route('/')
def main_route():
	options = {}
	return render_template("index.html", **options)
