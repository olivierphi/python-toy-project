
import flask
from .flask_get_current_weather import current_weather

app = flask.Flask(__name__)
app.register_blueprint(current_weather, url_prefix='/current')
