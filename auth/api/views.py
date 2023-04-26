from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
from auth.app import db
from auth.models.blocked_token import BlockedToken
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
        except KeyError:
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
                pwd_hash = generate_password_hash(password)

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
    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']

            # Fetch user details
            user = User.query.filter_by(email=email).first()

            # User doesn't exist
            if not user:
                return make_response(
                    jsonify(create_response('failed', 'User not found'))), 404
            
            pwd_match = bcrypt.checkpw(
                password=encode_to_bytes(password),
                hashed_password=encode_to_bytes(user.password))
            
            # password is not correct
            if not pwd_match:
                response = create_response('failed', 'Incorrect Password')
                return make_response(jsonify(response)), 401

            # User password is correct, generate a new JWT auth token
            response = create_response(status='success',
                message='User login successful.')
            response['jwt_token'] = encode_jwt_token(user.id)

            return make_response(jsonify(response)), 200

        except KeyError:
            response = create_response('failed', 'Email / Password missing')
            return make_response(jsonify(response)), 401
        except Exception as e:
            response = create_response('failed', 'Internal Error')
            return make_response(jsonify(response)), 500

class LogoutAPI(MethodView):
    def post(self):
        try:
            # verify if the user is authorized by checking the JWT auth token
            jwt_token = extract_jwt_token(request.headers)
            is_valid, user_id, err_message, status_code = is_valid_jwt(jwt_token)

            # invalid JWT token
            if not is_valid:
                response = create_response('failed', err_message)
                return make_response(jsonify(response)), status_code

            # JWT is valid, block the token
            block_jwt_token(jwt_token=jwt_token)
            response = create_response('success', 'Logout Successful')
            return make_response(jsonify(response)), 200

        except Exception as e:
            response = create_response('failed', 'Internal Error')
            return make_response(jsonify(response)), 500

class UserAPI(MethodView):
    def get(self):
        try:
            # verify if the user is authorized by checking the JWT auth token
            jwt_token = extract_jwt_token(request.headers)
            is_valid, user_id, err_message, status_code = is_valid_jwt(jwt_token)

            # invalid JWT token
            if not is_valid:
                response = create_response('failed', err_message)
                return make_response(jsonify(response)), status_code

            # JWT decoding was successful, fetch user details
            user = User.query.filter_by(id=user_id).first()

            # User doesn't exist
            if not user:
                return make_response(jsonify(create_response('failed', 'User not found'))), 404

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

