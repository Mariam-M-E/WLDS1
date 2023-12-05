import pytest
from .. import create_app, db, auth
from ..models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h2>Welcome to our Water Leakage Detection System</h2>' in response.data
    
def test_detect_leak_access_logged_in(client, app):
    with app.app_context():
        # add a user and login, since accsesing this page requirs login
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        response = client.post('/detect_leak',follow_redirects=True)

        assert response.status_code == 200
        assert b'<h2>Choose Your Mission</h2>' in response.data
        
def test_detect_leak_access_not_logged_in(client, app):
    response = client.get('/detect_leak', follow_redirects=False)
    assert response.status_code == 302          


def test_start_new_mission_access_logged_in(client, app):
    # page cant be accsesed unlees user is loged in
    with app.app_context():
        # add a user and login, since accsesing this page requirs login
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        
def test_start_new_mission_access_not_logged_in(client, app):
    # page cant be accsesed unlees user is loged in
    response = client.get('/start_mission', follow_redirects=False)
    assert response.status_code == 302  


def test_start_new_mission_valid(client, app):

    with app.app_context():
        # need to login since page can only be accessed by loged in user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        #  valid pipe and device id
        response = client.post('/start_mission', data={'pipe_id': '1', 'device_id': '1'}, follow_redirects=True)

        assert response.status_code == 200
        assert b'<div class="flash-message alert alert-success">' in response.data
        
def test_start_new_mission_invalid_pipeID(client, app):

    with app.app_context():
        # need to login since page can only be accessed by loged in user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        # invalid pipe ID
        response = client.post('/start_mission', data={'pipe_id': 'invalid', 'device_id': '2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Invalid Pipe ID' in response.data
def test_start_new_mission_invalid_deviceID(client, app):

    with app.app_context():
        # need to login since page can only be accessed by loged in user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        # invalid device ID
        response = client.post('/start_mission', data={'pipe_id': '2', 'device_id': 'invalid'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Invalid Device ID' in response.data
        
def test_start_new_mission_pipe_not_available(client, app):

    with app.app_context():
        # need to login since page can only be accessed by loged in user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        response = client.post('/start_mission', data={'pipe_id': '1', 'device_id': '1'}, follow_redirects=True)

        assert response.status_code == 200
        # pipe already in use
        response = client.post('/start_mission', data={'pipe_id': '1', 'device_id': '2'}, follow_redirects=True)
        # assert response.status_code == 200
        assert b'Invalid Pipe ID' in response.data

            
def test_start_new_mission_Device_not_available(client, app):
    with app.app_context():
        # need to login since page can only be accessed by loged in user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)
        assert login_response.status_code == 200
        
        response = client.post('/start_mission', data={'pipe_id': '1', 'device_id': '1'}, follow_redirects=True)
        assert response.status_code == 200
        # device already in use
        response = client.post('/start_mission', data={'pipe_id': '2', 'device_id': '1'}, follow_redirects=True)
        # assert response.status_code == 200
        assert b'Invalid Device ID' in response.data
        

def tearDown(self):
    with self.app.app_context():
        db.drop_all()