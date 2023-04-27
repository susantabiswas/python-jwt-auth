# Python Authentication System

[![CodeQL](https://github.com/susantabiswas/python-jwt-template/actions/workflows/codeql.yml/badge.svg)](https://github.com/susantabiswas/python-jwt-template/actions/workflows/codeql.yml)

Authentication is one of the most important things one would want in a service.
This is an authentication system using JWT.

This project is not a ready to use production system but rather shows the various aspects involved for making an authentication service. 

> JWT is a widely used authentication method for backend APIs. It allows users to securely access resources by providing a token that verifies their identity. This token contains encoded user information and is validated by the server for each request.

# Table of Contents
- [Python Authentication System](#python-authentication-system)
- [Table of Contents](#table-of-contents)
- [Project Setup](#project-setup)
  - [Clone the repo](#clone-the-repo)
  - [Install Dependencies](#install-dependencies)
  - [Setup Databases](#setup-databases)
    - [Run MySQL via Docker](#run-mysql-via-docker)
  - [Run Tests](#run-tests)
  - [Run the Server](#run-the-server)
    - [Flask server](#flask-server)
    - [Database related operations](#database-related-operations)
  - [Postman API collection](#postman-api-collection)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
    - [Salient points](#salient-points)
- [Usage](#usage)
  - [Driver file](#driver-file)
  - [REST APIs](#rest-apis)
    - [Register a user](#register-a-user)
    - [Login](#login)
    - [Logout](#logout)
    - [User details](#user-details)
- [Scope of Improvement](#scope-of-improvement)
- [References](#references)

# Project Setup
The code was tested with python 3.10.

## Clone the repo

```
git clone https://github.com/susantabiswas/python-jwt-auth
cd python-jwt-auth
```

## Install Dependencies
I would recommend using a virtual environment to avoid any version collisions and conflicts.

**For anaconda/miniconda**
```
conda create -n env python=3.10
conda activate env
```

**For venv**
```
python -m venv env

# For windows
.\env\bin\activate

# For Linux
source env/bin/activate
```

```
pip install -r requirements.txt
```

## Setup Databases
Ensure that a mysql database is up and running. MySQL is used for storing the users and blocked tokens.

### Run MySQL via Docker
```
docker pull mysql:latest
docker run -d -p 3306:3306 --name mysql-docker -e MYSQL_ROOT_PASSWORD=root mysql:latest

mysql -uroot -P3306 -h127.0.0.1 -p

# Once inside the mysql shell
CREATE DATABASE flask_jwt
CREATE DATABASE flask_jwt_test
```

Modify the .env file and update `TEST_DATABASE_URI` and `DATABASE_URI`

Run the command to perform the database migrations.
```
python app.py --create
```

## Run Tests
This will run the unit tests and generate coverage report
```
python -m coverage run -m unittest

# generate coverage report
python -m coverage html
```
This will generate a html report which can be viewed by running a liveserver from the htmlcov directory.

## Run the Server
This will start the flask server
```
python app.py --server
```

> You can also directly use the flask shell to execute
### Flask server
```
flask run
```

### Database related operations
```
# Creates migration folder
flask db init

# Creates migration operations to perform
flask db migrate

# Actual migration is performed. This will create the databases
# or any schema changes
flask db upgrade

# Revert the last migration
flask db downgrade
```

## Postman API collection
Here is a postman [API Collection](https://github.com/susantabiswas/python-jwt-template/blob/main/data/Flask%20JWT%20Auth.postman_collection.json) that can be used via importing it.


# Project Structure
```
.
├── LICENSE
├── README.md
├── app.py
├── auth
│   ├── api
│   │   ├── auth_utils.py
│   │   └── views.py
│   ├── app.py
│   ├── config.py
│   └── models
│       ├── blocked_token.py
│       └── user.py
├── requirements.txt
└── tests
    ├── __init__.py
    ├── api_base.py
    ├── base.py
    ├── test_apis.py
    ├── test_auth_utils.py
    ├── test_config.py
    └── test_models.py
```

# Architecture

### Salient points
>
    1. Password Hashing 
    2. JWT Token generation
    3. JWT token invalidation/blocking
    4. High code coverage using unittest


# Usage
## Driver file
`app.py` in the projeect root is the main driver file. It support command line arguments and can be used for running the server.
```
python app.py --help
```
```
usage: app.py [-h] (-c | -d | -s)

options:
  -h, --help    show this help message and exit
  -c, --create  Initialize database tables     
  -d, --drop    Delete all the database tables 
  -s, --server  Start the flask server
```

## REST APIs
The authentication system supports the following APIs:

### Register a user
Adds a new user to the system
```
/auth/signup
```

### Login
Verifies the credentials and returns a auth JWT
```
/auth/login
```
### Logout
Logs the user out and invalidates the JWT associated with it.
```
/auth/logout
```

### User details
User resource related operations
```
/auth/user
```

# Scope of Improvement
- Use Redis for BlockedToken resource with TTL to auto-clear them from DB.
- Add Swagger spec
- Add data validation for the models

# References
There are lot of things used in the project and the following links might be helpful for further reading.

https://susantabiswas.com/posts/Practical-JSON-Web-Tokens-(JWT)-guide

https://pypi.org/project/PyJWT/

https://pythonhosted.org/Flask-Testing/

https://stackoverflow.com/questions/56622797/using-flask-migrate-for-models-in-multiple-files

https://flask-migrate.readthedocs.io/en/latest/

https://zetcode.com/python/bcrypt/

https://realpython.com/token-based-authentication-with-flask/

https://blog.miguelgrinberg.com/post/how-to-add-flask-migrate-to-an-existing-project

https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

https://hackersandslackers.com/configure-flask-applications/
