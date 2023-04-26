from os import environ
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from auth.config import export_environment_variables

# Load the environment vars from the local env file
export_environment_variables()

# Create the Flask server and load the configs from the configuration
# file. Some of the settings in the configuration file are taken from
# environment variables
app = Flask(__name__)
app.config.from_object(
    environ.get("APP_ENVIRONMENT",
                "auth.config.DevConfig"))
CORS(app)


# Setup the objects for handling database migration.
# If there is any schema change, this will apply the changes to
# the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from auth.api.views import auth_blueprint
from auth.models.blocked_token import BlockedToken
from auth.models.user import User

app.register_blueprint(auth_blueprint)
