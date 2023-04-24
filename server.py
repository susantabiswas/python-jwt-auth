from flask import Flask
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)

server.config.from_object("APP_SETTINGS")

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000)