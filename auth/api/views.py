from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from auth.app import db
from auth.models.token_blocklist import TokenBlocklist
from auth.models.user import User

auth_blueprint = Blueprint("auth", __name__)

class SignupAPI(MethodView):
    pass

class LoginAPI(MethodView):
    pass

class LogoutAPI(MethodView):
    pass

class UserAPI(MethodView):
    pass



