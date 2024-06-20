from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth
from flask_httpauth import HTTPTokenAuth
import jwt
from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from flask_app.models import User


class BricksGlobalObjects():
    def init_global_objects(self, app: Flask):
        ''' Call this method in Flask application factory create_app 
            to initialize the global objects of 3rd party extensions. '''
        self.db_engine = create_engine(app.config['DB_URL'], echo=app.config['SQLALCHEMY_ECHO'])
        self.db_session = scoped_session(sessionmaker(bind=self.db_engine))

        self.oauth = OAuth(app)
        self.flask_auth = HTTPTokenAuth(scheme='Bearer')
        self.init_flask_auth(app)
        self.google_oauth = self.init_google_oauth(app)

    def init_flask_auth(self, app: Flask):
        ''' Initialize Flask authentication object '''
        @self.flask_auth.verify_token
        def verify_token(token):
            '''decode the JWT and verify the user identity'''
            try:
                data = jwt.decode(token,
                                app.config['SECRET_KEY'],
                                algorithms=['HS256'])
            except:
                return False

            if time() > data['exp']:
                # the JWT is expired
                return False
            
            user = GlobalObjects.db_session.query(User).filter(User.user_email==data['user_email']).first()
            if user is None:
                return False
            return user

        @self.flask_auth.error_handler
        def auth_error(status):
            response_object = {
                "message":"Access Denied",
                "status":"failure"
            }
            if status == 403:
                response_object['message'] = "Permission Denied"
            return jsonify(response_object), status


    def init_google_oauth(self, app: Flask):
        ''' Initialize Google OAuth object '''
        google_oauth = self.oauth.register(
            name='google', # name of this method
            client_id = app.config['GOOGLE_OAUTH_CLIENT_ID'],
            client_secret = app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
            access_token_url='https://oauth2.googleapis.com/token',
            access_token_params=None,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            api_base_url='https://accounts.googleapis.com/oauth2/v3',
            client_kwargs={'scope': 'openid profile email'},
            server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
            jwk_uri='https://www.googleapis.com/oauth2/v3/certs'
        )
        return google_oauth
    
    def __str__(self):
        return f"SQLAlchemy object type : {type(self.db_session)}\
                \nOAuth object type : {type(self.oauth)}\
                \nGoogle OAuth object type : {type(self.google_oauth)}\
                \nFlask authenticator object tyoe : {type(self.flask_auth)}"


GlobalObjects = BricksGlobalObjects()

