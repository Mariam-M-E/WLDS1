import unittest
from flask import Flask
from ..models import db, Pipe, Device, Mission, User

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_pipe_creation(self):
        # Test creating a Pipe instance and saving it to the database
        with self.app.app_context():
            pipe = Pipe(start_point='A', end_point='B', diameter=10.0, water_pressure=20.0, length=30.0)
            db.session.add(pipe)
            db.session.commit()

            saved_pipe = Pipe.query.filter_by(start_point='A').first()

            self.assertIsNotNone(saved_pipe)
            self.assertEqual(saved_pipe.start_point, 'A')
            self.assertEqual(saved_pipe.end_point, 'B')
            self.assertEqual(saved_pipe.diameter, 10.0)
            self.assertEqual(saved_pipe.water_pressure, 20.0)
            self.assertEqual(saved_pipe.length, 30.0)
            self.assertEqual(Pipe.query.count(), 1)
            self.assertEqual(pipe.status, 'available')

    def test_device_creation(self):
        with self.app.app_context():
            device = Device(model='TestModel', diameter=15.0)
            db.session.add(device)
            db.session.commit()

            saved_device = Device.query.filter_by(model='TestModel').first()

            self.assertIsNotNone(saved_device)
            self.assertEqual(saved_device.model, 'TestModel')
            self.assertEqual(saved_device.diameter, 15.0)
            self.assertEqual(Device.query.count(), 1)
            self.assertEqual(device.status, 'available')

    def test_mission_creation(self):
        with self.app.app_context():
            pipe = Pipe(start_point='A', end_point='B', diameter=10.0, water_pressure=20.0, length=30.0)
            db.session.add(pipe)
            device = Device(model='TestModel', diameter=15.0)
            db.session.add(device)
            db.session.commit()

            mission = Mission(pipe_id=pipe.id, device_id=device.id)
            db.session.add(mission)
            db.session.commit()
            saved_mission = Mission.query.filter_by(pipe_id=pipe.id, device_id=device.id).first()

            self.assertIsNotNone(saved_mission)
            self.assertEqual(saved_mission.pipe_id, pipe.id)
            self.assertEqual(saved_mission.device_id, device.id)
            self.assertEqual(saved_mission.status, 'active')
            self.assertEqual(Mission.query.count(), 1)
            self.assertEqual(pipe.status, 'inUse')
            self.assertEqual(device.status, 'inUse')
            
    def test_create_user(self):
        # Test creating a user instance
        user = User(email='test@example.com', password='password', first_name='tester')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

            self.assertEqual(User.query.count(), 1)
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.password, 'password')
            self.assertEqual(user.first_name, 'tester')
        
    def test_unique_email(self):
        # Test the unique constraint on the email field
        user1 = User(email='test@example.com', password='password', first_name='tester')
        user2 = User(email='test@example.com', password='another_password', first_name='tester2')
        with self.app.app_context():
            db.session.add(user1)
            db.session.commit()

        # Attempting to add a user with the same email should raise an Integrity error
            with self.assertRaises(Exception):
                db.session.add(user2)
                db.session.commit()

if __name__ == '__main__':
    unittest.main()