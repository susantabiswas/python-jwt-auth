from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from os import path, environ

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

from models.user import User
from models.token_blocklist import TokenBlocklist

if __name__ == "__main__":
    app.run(
        host=app.config['HOST'],
        port=app.config['FLASK_PORT'])