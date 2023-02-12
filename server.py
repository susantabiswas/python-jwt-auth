import os
import jwt
import datetime
from flask import Flask, request, make_response, jsonify
from flask_mysqldb  import MySQL
import configparser

server = Flask(__name__)
auth_users_db = MySQL(server)
blocked_tokens_db = MySQL(server)

CONFIG_FILENAME = "./python-jwt-template/config.ini"
CONFIG_HEADER = "JwtApp"
config = configparser.ConfigParser()
config.read(CONFIG_FILENAME)

# Mysql settings
server.config["MYSQL_HOST"] = config.get(CONFIG_HEADER, "MYSQL_HOST")
server.config["MYSQL_USER"] = config.get(CONFIG_HEADER,"MYSQL_USER")
server.config["MYSQL_PASSWORD"] = config.get(CONFIG_HEADER,"MYSQL_PASSWORD")
server.config["MYSQL_DB"] = config.get(CONFIG_HEADER,"MYSQL_DB")
server.config["MYSQL_PORT"] = int(config.get(CONFIG_HEADER,"MYSQL_PORT"))

@server.route("/register", methods=["POST"])
def register():
    pass

@server.route("/login", methods=["POST"])
def login():
    # get the auth header contents
    auth_header = request.authorization
    if not auth_header:
        return "Credential details missing", 401

    # check whether the user is registered or not
    cursor = auth_users_db.connection.cursor()

    query = """SELECT email, password FROM users WHERE email='{}'""".format(auth_header.username)
    result = cursor.execute(query)

    if result > 0:
        row = cursor.fetchone()
        email = row[0]
        pwd = row[1]

        if auth_header.username != email or auth_header.password != pwd:
            return "Invalid credentials", 401
        else:
            responseObject = {
                    'status': 'verified',
                    'message': 'User verified.'
                }
            return make_response(jsonify(responseObject)), 200
    else:
        return "Invalid credentials", 401

@server.route("/auth", methods=["POST"])
def auth():
    pass

@server.route("/logout", methods=["POST"])
def logout():
    pass


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000)