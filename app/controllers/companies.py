from flask import render_template, Blueprint

companies = Blueprint('companies', __name__, template_folder='views')

@companies.route('/companies')
def companies_route():
	options = {}
	return render_template("companies.html", **options)
