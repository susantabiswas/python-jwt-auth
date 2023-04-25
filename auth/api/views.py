from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
import jwt
from auth.app import db
from auth.models.token_blocklist import TokenBlocklist
from auth.models.user import User
from auth.api.auth_utils import *
import bcrypt

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
        except Exception:
            response = create_response(status='failed',
                    message='Required fields are missing.')
            return make_response(jsonify(response)), 400

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()

        # User already exists
        if user:
            response = create_response(status='failed',
                    message='User already exists.')
            return make_response(jsonify(response)), 202
        else:
            try:
                # hash the password and then save it. This ensures that in the event
                # the data is exposed, the actual passwords won't be exposed
                pwd_salt = bcrypt.gensalt(app.config['BCRYPT_ROUNDS'])
                # the password needs to be converted to byte-array to get the hash
                pwd_hash = bcrypt.hashpw(password.encode('utf-8'), pwd_salt)

                # Insert the User record in database
                user = User(email=email, password=pwd_hash, name=name)
                db.session.add(user)
                db.session.commit()

                # generate the JWT token and send it with the response
                response = create_response(status='success',
                    message='User signed up successful.')
                response['jwt_token'] = encode_jwt_token(user.id)

                return make_response(jsonify(response)), 201
            except Exception as e:
                response = create_response('failed', 'Internal Error')
                return make_response(jsonify(response)), 500


class LoginAPI(MethodView):
    pass

class LogoutAPI(MethodView):
    pass

class UserAPI(MethodView):
    def get(self):
        try:
            # verify if the user is authorized by checking the JWT auth token
            is_valid, user_id, err_message, status_code = is_valid_jwt(request.headers)

            # invalid JWT token
            if not is_valid:
                response = create_response('failed', err_message)
                return make_response(jsonify(response)), status_code

            # JWT decoding was successful, fetch user details
            user = User.query.filter_by(id=user_id).first()
            response = create_response('success', '')
            response['details'] = {
                'email': user.email,
                'name': user.name,
                'admin': user.admin,
                'registration_on': user.registration_timestamp
            }
            return make_response(jsonify(response)), 200
        except Exception:
            return make_response(jsonify(create_response('failed', 'Internal Error'))), 500


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

