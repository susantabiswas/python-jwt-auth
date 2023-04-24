from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create the Flask server and load the configs from the configuration
# file. Some of the settings in the configuration file are taken from
# environment variables
app = Flask(__name__)
app.config.from_object("config.DevConfig")

# Setup the objects for handling database migration.
# If there is any schema change, this will apply the changes to
# the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, TokenBlocklist

if __name__ == "__main__":
    app.run(
        host=app.config['HOST'],
        port=app.config['FLASK_PORT'])