from os import environ, path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

APP_ENV_FILE = ".env"
# Load the environment vars from the local env file
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, APP_ENV_FILE))


# Create the Flask server and load the configs from the configuration
# file. Some of the settings in the configuration file are taken from
# environment variables
app = Flask(__name__)
app.config.from_object(environ.get("APP_ENVIRONMENT"))

# Setup the objects for handling database migration.
# If there is any schema change, this will apply the changes to
# the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from auth.models.token_blocklist import TokenBlocklist
from auth.models.user import User

if __name__ == "__main__":
    app.run(
        host=app.config['HOST'],
        port=app.config['FLASK_PORT'])