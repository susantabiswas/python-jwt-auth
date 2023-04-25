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


# define the views for the APIs
signup_api = SignupAPI.as_view('signup_api')
login_api = LoginAPI.as_view('login_view')
logout_api = LogoutAPI.as_view('logout_view')
user_api = UserAPI.as_view('user_view')

auth_blueprint.add_url_rule(
    '/auth/signup',
    view_func=signup_api,
    methods=["GET"]
)

auth_blueprint.add_url_rule(
    'auth/login',
    view_func=login_api,
    methods=["POST"]
)

auth_blueprint.add_url_rule(
    'auth/logout',
    view_func=logout_api,
    methods=["POST"]
)

auth_blueprint.add_url_rule(
    'auth/user',
    view_func=user_api,
    methods=["GET"]
)

