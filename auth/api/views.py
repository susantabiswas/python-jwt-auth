from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from auth.app import db
from auth.models.token_blocklist import TokenBlocklist
from auth.models.user import User

auth_blueprint = Blueprint("auth", __name__)

class SignupAPI(MethodView):
    def post(self):
        # Get the post data
        data = request.get_json()

        # Check if the required fields are present or not
        email, password, name = None, None, None
        try:
            email = data['email']
            password = data['password']
            name = data['name']
        except Exception as e:
            response = {
                'status' : 'failed',
                'message': 'Required fields are missing.'
            }
            return make_response(jsonify(response)), 400

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()

        if user:
            response = {
                'status': 'failed',
                'message': 'User already exists.'
            }
            return make_response(jsonify(response)), 202
        else:
            try:
                user = User(email=email, password=password, name=name)
                db.session.add(user)
                db.session.commit()

                # generate the JWT token
                response = {
                    'status': 'success',
                    'message': 'User signed up successful.'
                }
                return make_response(jsonify(response)), 201
            except:
                response = {
                    'status': 'failed',
                    'message': 'Internal error'
                }
                return make_response(jsonify(response)), 500


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
    methods=["POST"]
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_api,
    methods=["POST"]
)

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_api,
    methods=["POST"]
)

auth_blueprint.add_url_rule(
    '/auth/user',
    view_func=user_api,
    methods=["GET"]
)

