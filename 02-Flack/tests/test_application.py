import pytest
import application
import json

# Note:
# To run tests on local system, use "python3 -m pytest --disable-warnings"

@pytest.fixture
def client():
     application.app.config['TESTING'] = True
     testing_client = application.app.test_client()
     yield testing_client


### HOME PAGE
def test_root(client):
    rv = client.get('/', follow_redirects=True)
    assert b'Flack' in rv.data

### join-chat

def test_index(client):
    rv = client.get('/join-chat')
    assert b'Join the chat' in rv.data


def test_blank_username(client):
    username = ""

    rv = client.post('/join-chat', data=dict(
        username=username
    ), follow_redirects=True)

    assert b'Username cannot be blank.' in rv.data

def test_username_with_blankspaces(client):
    username = "a\nb\tb\fc\r"

    rv = client.post('/join-chat', data=dict(
        username=username
    ), follow_redirects=True)

    assert b'Username cannot have white spaces in it.' in rv.data
