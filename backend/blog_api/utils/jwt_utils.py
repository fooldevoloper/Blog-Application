import jwt
import datetime
from decouple import config
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

# JWT configuration
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='default_jwt_secret_key')
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_EXPIRATION_DELTA = config('JWT_EXPIRATION_DELTA', default=3600, cast=int)


def generate_token(user_id):
    """
    Generate a JWT token for a user.
    
    Args:
        user_id (int): The ID of the user.
        
    Returns:
        str: The JWT token.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_DELTA),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token):
    """
    Verify a JWT token and return the user ID.
    
    Args:
        token (str): The JWT token.
        
    Returns:
        int: The user ID if token is valid.
        
    Raises:
        jwt.ExpiredSignatureError: If token has expired.
        jwt.InvalidTokenError: If token is invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload['user_id']
        return user_id
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")