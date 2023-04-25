from datetime import datetime, timedelta
import jwt
from auth.app import app
from flask import request
from auth.app import db
from auth.models.token_blocklist import BlockedToken 

def encode_jwt_token(user_id: str)->str:
    """Creates a JWT auth token. Uses a symmetric algorithm for
    signing the token.

    Args:
        user_id (str): Unique user id

    Raises:
        e: Exception

    Returns:
        str: Encrypted token signature
    """
    try:
        curr_time = datetime.utcnow()

        payload = {
            'sub': user_id,
            'iat': curr_time,
            'exp': curr_time +  timedelta(days=0, minutes=10, seconds=0)
        }
        return jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256' # We will use a symmetric algorithm
        )
    except Exception as e:
        raise e

def decode_jwt_token(jwt_token: str)->str:
    """Decodes a JWT token signature

    Args:
        jwt_token (str): JWT token

    Raises:
        InvalidTokenError: If jwt token is invalid
        ExpiredSignatureError: If the jwt token is expired
        e: Any other exception

    Returns:
        str: Unique user id
    """
    payload = jwt.decode(
        jwt_token,
        app.config['SECRET_KEY'],
        algorithms=["HS256"])
    return payload['sub']


def create_response(status: str, message: str)->dict:
    """Creates the standard response body

    Args:
        status (str): Status of operation
        message (str): Message for response

    Returns:
        dict: Dict representing the fields as key
    """
    return {
        'status': status,
        'message': message
    }

def extract_jwt_token(req_headers)->str:
    """Extracts the JWT auth token from Authorization header
    if present

    Args:
        req_header (Request Headers)

    Returns:
        JWT token: JWT auth token
    """
    # Authorization: Bearer <JWT token>
    auth_header = req_headers.get('Authorization')
    jwt_token = auth_header.split(' ')[1] if auth_header else None
    return jwt_token

def is_valid_jwt(jwt_token):
    """Checks whether the header has a valid JWT token or not.

    Args:
        jwt_token(str): JWT auth token

    Returns:
        is_valid (bool): Whether the JWT token is valid
        jwt_payload_output (str): Output from payload
        err_message (str): In case of exception, saves the exception message
            otherwise None
        status_code(int) : Status code
    """
    # JWT token is not passed
    if jwt_token is None:
        return False, "Authorization header missing", 401
    
    try:
        user_id = decode_jwt_token(jwt_token=jwt_token)
        # JWT token has not been tampered with. Next
        # check if the token is blocked or not

        # JWT token is blocked
        if is_jwt_blocked(jwt_token=jwt_token):
            return False, None, "JWT token is blocked. Please login again", 401
        return True, user_id, None, 200
    
    except jwt.InvalidSignatureError as e:
        return False, None, "Token Signature doesn't match", 401
    except jwt.ExpiredSignatureError as e:
        return False, None, "Signature is expired. Please log in again to refresh", 401
    except jwt.InvalidTokenError as e:
        return False, None, "Invalid token signature", 401

def is_jwt_blocked(jwt_token: str)->bool:
    blocked_token = BlockedToken.query.filter_by(token=jwt_token).first()
    return blocked_token is not None
    
