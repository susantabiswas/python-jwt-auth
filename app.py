from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("config.DevConfig")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, TokenBlocklist

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['FLASK_PORT'])