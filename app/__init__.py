from flask import Flask, render_template
import config

app = Flask(__name__, template_folder='views')
app.config.from_object(config)

import controllers

# Register blueprints
app.register_blueprint(controllers.calendar)
app.register_blueprint(controllers.companies)
app.register_blueprint(controllers.contact)
app.register_blueprint(controllers.events)
app.register_blueprint(controllers.join)
app.register_blueprint(controllers.main)

@app.errorhandler(401)
def custom_401(error, url="srapq281tt9/pa2"):
	return "Error 401 - Not authorized."

@app.errorhandler(404)
def not_found(err):
	return "Error 404 - Not found"

if __name__ == '__main__':
    # listen on external IPs
    app.run(host='localhost', port=config.PORT, debug=config.DEBUG)