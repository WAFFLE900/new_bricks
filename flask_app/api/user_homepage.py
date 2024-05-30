from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import User
from flask_app.auth import make_JWT, hash_password
import logging

bp = Blueprint('user_homepage', __name__)