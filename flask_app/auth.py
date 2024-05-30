from flask import current_app
import jwt
import hashlib
from time import time

def hash_password(password):
    '''The function hashes the input password'''
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

def make_JWT(user_email):
    '''The function create the JWT for a login user'''
    token = jwt.encode(
        {
            'user_email': user_email,
            'exp': int(time() + 60 * 60 * 24 * 30)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256')
    return token
