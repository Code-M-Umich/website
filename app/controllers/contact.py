from flask import render_template, Blueprint

contact = Blueprint('contact', __name__, template_folder='views')

@contact.route('/contact')
def contact_route():
	options = {}
	return render_template("contact.html", **options)
