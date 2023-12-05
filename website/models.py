from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Pipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="100")
    start_point = db.Column(db.String(100))
    end_point = db.Column(db.String(100))
    diameter = db.Column(db.Float)
    water_pressure = db.Column(db.Float)
    length = db.Column(db.Float)
    status = db.Column(db.String(150))
    
    def __init__(self, start_point, end_point, diameter, water_pressure, length):
        self.start_point = start_point
        self.end_point = end_point
        self.diameter = diameter
        self.water_pressure = water_pressure
        self.status = "available"
        self.length = length

    @classmethod
    def get_Available_Pipes(cls):
        return cls.query.filter_by(status='available').all()
    
    def set_pipe_status(self, status):
        self.status = status
        
    @classmethod
    def validate_pipe_ID(cls, pipe_id):
        existing_pipe = cls.query.filter_by(id=pipe_id, status='available').first()
        return existing_pipe is not None

    @classmethod
    def print_info(cls, pipe_id):
        pipe = db.session.get(Pipe, pipe_id)
        if pipe:
            print(f"Pipe ID: {pipe.id}")
            print(f"Start Point: {pipe.start_point}")
            print(f"End Point: {pipe.end_point}")
            print(f"Diameter: {pipe.diameter}")
            print(f"Water Pressure: {pipe.water_pressure}")
        else:
            print(f"Pipe with ID {pipe_id} not found.")


    
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100))
    diameter = db.Column(db.Float)
    status = db.Column(db.String(150))
    
    def __init__(self, model, diameter):
        self.model = model
        self.diameter = diameter
        self.status = "available"
    @classmethod    
    def get_Available_Divices(cls):
        return cls.query.filter_by(status='available').all()
    
    def set_device_status(self, status):
        self.status = status
    
    @classmethod
    def validate_device_ID(cls, device_id):
        existing_device = cls.query.filter_by(id=device_id,status='available').first()
        return existing_device is not None
    @classmethod
    def print_info(cls, device_id):
        device = db.session.get(Device, device_id)
        if device:
            print(f"Device ID: {device.id}")
            print(f"Model: {device.model}")
            print(f"Diameter: {device.diameter}")
        else:
            print(f"Device with ID {device_id} not found.")

    
class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pipe_id = db.Column(db.Integer, db.ForeignKey('pipe.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(150))


    def __init__(self, pipe_id, device_id):
        self.pipe_id = pipe_id
        self.device_id = device_id
        self.status = "active"
        self.date_created = datetime.utcnow()
        
        pipe = db.session.get(Pipe, pipe_id)
        if pipe:
            pipe.set_pipe_status("inUse")
            
        device = db.session.get(Device, device_id)
        if device:
            device.set_device_status("inUse")
            
    def __repr__(self):
        return f'<Mission {self.id}>'

    @classmethod
    def print_info(self):
        print(f"Mission ID: {self.id}")
        print(f"Pipe ID: {self.pipe_id}")
        print(f"Device ID: {self.device_id}")
        print(f"Date Created: {self.date_created}")
        print(f"Status: {self.status}")
        # Call print functions for Pipe and Device
        Pipe.print_info(self.pipe_id)
        Device.print_info(self.device_id)
       
    def get_mission_info(self):

        mission_info = {
            'mission_id': self.id,
            'date_created': self.date_created,
            'status': self.status
        }
        # Retrieve pipe information
        pipe = db.session.get(Pipe, self.pipe_id)
        if pipe:
            mission_info['pipe'] = {
                'pipe_id': pipe.id,
                'start_point': pipe.start_point,
                'end_point': pipe.end_point,
                'diameter': pipe.diameter,
                'water_pressure': pipe.water_pressure,
                'length': pipe.length
            }
        else:
            mission_info['pipe'] = None
        # Retrieve device information
        device = db.session.get(Device, self.device_id)
        if device:
            mission_info['device'] = {
                'device_id': device.id,
                'model': device.model,
                'diameter': device.diameter
            }
        else:
            mission_info['device'] = None
        return mission_info

