import pytest
from flask_app.app import create_app

from flask_app.models import db, User

@pytest.fixture()
def app():
    app = create_app(
        test_mode=True,
        config_dict={
            "TESTING": True,
            "DB_URL": "sqlite+pysqlite:///test.db",
            "SQLALCHEMY_DATABASE_URI": "sqlite+pysqlite:///test.db"
        }
    )

    # other setup can go here
    db.init_app(app)

    user = User()
    db.session

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='bricksBE@gmail.com', password='Bricks1234'):
        return self._client.post(
            '/bricks_login',
            json={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/bricks_logout')


@pytest.fixture()
def auth(client):
    return AuthActions(client)