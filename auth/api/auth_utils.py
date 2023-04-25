from datetime import datetime, timedelta
import jwt
from auth.app import app

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