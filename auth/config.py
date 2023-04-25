from dotenv import load_dotenv
from os import environ, path

def export_environment_variables(env_filename=".env") -> None:
    """Exports the environment variables from the .env file.

    Args:
        env_file_name (str, optional): local environment file containing the variables. Defaults to ".env".
    """
    # Load the environment vars from the local env file
    BASE_DIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(BASE_DIR, env_filename))
    
# Load the environment vars from the local env file
export_environment_variables()

class BaseConfig:
    # Flask config
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    FLASK_PORT = 5000
    BCRYPT_ROUNDS = 4
    PROPAGATE_EXCEPTIONS = False
    # Database config
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
    
    # MySQL
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306

class ProdConfig(BaseConfig):
    FLASK_ENV = "production"
    DEBUG = False

    # MySQL
    MYSQL_HOST = ""
    MYSQL_PORT = 3306

