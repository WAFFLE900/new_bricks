from flask_app.app import create_app
from conftest import client

def test_config():
    assert not create_app().testing

def test_bricks(client):
    response = client.get('/bricks')
    assert response.text == 'Bricks專案管理實用工具讚讚!'


def test_login(client, auth):
    assert client.get('/bricks_login').status_code == 200
    response = auth.login()
    assert response.headers["Authorization"] == "/"