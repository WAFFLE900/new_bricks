# from flask_app.app import create_app
from flask import Flask
from flask_app.models import db

app = Flask(__name__)
app.config.update({
    "SQLALCHEMY_DATABASE_URI": "sqlite+pysqlite:///test.db"
})

db.init_app(app)        # initialize a db object of Flask-SQLAlchemy

with app.app_context():
    db.create_all()         # create the sqlite database in memory from the ORM for unit tests
