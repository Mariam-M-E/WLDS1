import pytest
from flask import Flask, request, flash, redirect, url_for, render_template
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
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

def test_valid_login(client, app):
    with app.app_context():
        # add a user and login
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        with app.app_context():
            login_response = client.post('/login', data={'email': 'test@wlds.we', 'password': '1234567'}, follow_redirects=True)

            assert login_response.status_code == 200
            assert b'Home' in login_response.data


def test_invalid_password(client, app):
    with app.app_context():
        # add a user
        default_user = User(email='test@wlds.we', first_name="test", password=generate_password_hash('1234567'))
        db.session.add(default_user)
        db.session.commit()

        # attempt login with incorrect password
        with app.app_context():
            response = client.post('/login', data={'email': 'test@wlds.we', 'password': 'wrong_password'}, follow_redirects=True)

            assert response.status_code == 200
            assert b'Incorrect password' in response.data


def test_invalid_email(client, app):
    with app.app_context():
        # attempt login with nonexistent email
        with app.app_context():
            response = client.post('/login', data={'email': 'nonexistent@wlds.we', 'password': 'password'}, follow_redirects=True)

            assert response.status_code == 200
            assert b'Email does not exist' in response.data
