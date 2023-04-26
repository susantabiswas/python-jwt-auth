from datetime import datetime, timedelta
import jwt
from auth.app import app
from auth.app import db
from auth.models.blocked_token import BlockedToken
import bcrypt


def encode_jwt_token(user_id: str) -> str:
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
            'exp': curr_time +  timedelta(
                days=app.config['JWT_DAYS'],
                minutes=app.config['JWT_MINUTES'],
                seconds=app.config['JWT_SECONDS'])
        }
        return jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'  # We will use a symmetric algorithm
        )
    except Exception as e:
        raise e


def decode_jwt_token(jwt_token: str) -> str:
    """Decodes a JWT token signature

    Args:
        jwt_token (str): JWT token

    Raises:
        InvalidTokenError: If jwt token is invalid
        ExpiredSignatureError: If the jwt token is expired
        e: Any other exception

    Returns:
        str: JWT payload
    """
    payload = jwt.decode(
        jwt_token,
        app.config['SECRET_KEY'],
        algorithms=["HS256"])
    return payload


def create_response(status: str, message: str) -> dict:
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


def extract_jwt_token(req_headers) -> str:
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


def is_valid_jwt(jwt_token) -> bool:
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
        return False, None, "Auth token missing", 401
    try:
        jwt_payload = decode_jwt_token(jwt_token=jwt_token)
        # JWT token has not been tampered with. Next
        # check if the token is blocked or not

        # JWT token is blocked
        if is_jwt_blocked(jwt_token=jwt_token):
            return False, None, "JWT token is blocked. Please login again", 401
        return True, jwt_payload['sub'], None, 200
    except jwt.InvalidSignatureError as e:
        return False, None, "Token Signature doesn't match", 401
    except jwt.ExpiredSignatureError as e:
        return False, None, "Signature is expired. Please log in again to refresh", 401
    except jwt.InvalidTokenError as e:
        return False, None, "Invalid token signature", 401


def is_jwt_blocked(jwt_token: str) -> bool:
    """Checks whether a JWT token is blocked or not

    Args:
        jwt_token (str): JWT auth token

    Returns:
        bool: Whether the token is blocked
    """
    blocked_token = BlockedToken.query.filter_by(token=jwt_token).first()
    return blocked_token is not None


def block_jwt_token(jwt_token: str) -> None:
    """Blocks a JWT token by inserting its record in
    BlockedToken list

    Args:
        jwt_token (str): JWT token
    """
    jwt_payload = decode_jwt_token(jwt_token=jwt_token)
    blocked_token = BlockedToken(
        token=jwt_token,
        token_expiry=datetime.fromtimestamp(jwt_payload['exp']))
    # Add the token to the blockedToken DB
    db.session.add(blocked_token)
    db.session.commit()


def encode_to_bytes(s: str) -> bytes:
    """Encodes the string to bytes.

    Args:
        s (str): input string

    Returns:
        bytearray: string in bytes
    """
    return s.encode('utf-8')


def generate_password_hash(password: str) -> bytes:
    """Generates a hash of password using a salt

    Args:
        password (str): password

    Returns:
        bytes: Hashed password
    """
    pwd_salt = bcrypt.gensalt(app.config['BCRYPT_ROUNDS'])
    # the password needs to be converted to byte-array to get the hash
    pwd_hash = bcrypt.hashpw(encode_to_bytes(password), pwd_salt)

    return pwd_hash
