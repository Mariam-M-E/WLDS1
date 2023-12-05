from flask import Blueprint, get_flashed_messages, redirect, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required

import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def landing_page():
    return render_template("index.html")

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("engineer.html")

@views.route('/start_mission', methods=['GET', 'POST'])
@login_required
def start_new_mission():
    from .models import Mission, Pipe, Device
    from . import db
    new_mission_id = None  # Initialize the variable
    get_flashed_messages(with_categories=False)

    if request.method == 'POST':
        pipe_id = request.form.get("pipe_id")
        device_id = request.form.get("device_id")

        if Pipe.validate_pipe_ID(pipe_id):
            if Device.validate_device_ID(device_id):
                new_mission = Mission(pipe_id, device_id)
                db.session.add(new_mission)
                db.session.commit()
                new_mission_id = new_mission.id
                mission_info = new_mission.get_mission_info()

                flash(f'A New Mission Has Been Created! \nMission Summary - Mission ID: {new_mission_id} M-00 pipe ID: P-00{mission_info["pipe"]["pipe_id"]}, Pipe Length: {mission_info["pipe"]["length"]}, Device ID: D-00{mission_info["device"]["device_id"]}, Model: {mission_info["device"]["model"]}', category='success')

                return redirect(url_for('views.start_new_mission'))
            else:
                flash('Invalid Device ID', category='error')
                return redirect(url_for('views.start_new_mission'))
        else:
            flash('Invalid Pipe ID', category='error')
            return redirect(url_for('views.start_new_mission'))

    available_pipes = Pipe.get_Available_Pipes()
    available_devices = Device.get_Available_Divices()

    return render_template('new_mission.html', 
                           available_pipes=available_pipes, 
                           available_devices=available_devices, 
                           new_mission_id=new_mission_id)


@views.route('/detect_leak', methods=['GET', 'POST'])
@login_required
def detect_leak():

    return render_template('choose_m.html')

@views.route('/detect_leak1', methods=['GET', 'POST'])
@login_required
def detect_leak1():

    return render_template('detectleak1.html')

@views.route('/detect_leak2', methods=['GET', 'POST'])
@login_required
def detect_leak2():

    return render_template('detectleak2.html')

@views.route('/detect_leak3', methods=['GET', 'POST'])
@login_required
def detect_leak3():

    return render_template('detectleak2.html')


@views.route('/detect_leak_result', methods=['GET', 'POST'])
@login_required
def detect_leak_result():
    pipe_pressure = 40

    # Assuming you have measured_data as a list of pressure values
    measured_data = [
        45.0, 48.0, 50.0, 52.0, 55.0,
        60.0, 58.0, 55.0, 52.0, 50.0,
        48.0, 47.0, 45.0, 44.0, 42.0,
        40.0, 38.0, 35.0, 32.0, 30.0
    ]

    detection = [0] * len(measured_data)

    for i in range(len(measured_data)):
        if measured_data[i] < pipe_pressure * 0.95:  # Assuming 5% threshold for detection
            detection[i] = 1

    # Loop to find leak size
    leak_sizes = []
    current_leak_size = 0

    for i, value in enumerate(detection):
        if value == 1:
            current_leak_size += 1
            if current_leak_size == 3:  # Assuming 3 consecutive detections indicate a leak size
                leak_sizes.append(current_leak_size)
                current_leak_size = 0
        else:
            current_leak_size = 0

    # Calculate water loss estimate
    water_loss_estimates = [size * (pipe_pressure - measured_data[i]) for i, size in enumerate(detection) if size == 1]

    # Prepare output
    result = {
        'mission_id': "M-021",
        'city': "ABU DHABI",
        'pipe_id': "P-034",
        'device_id': "D-004",
        'leak_detected': any(detection),
        'leak_locations': [i for i, value in enumerate(detection) if value == 1],
        'leak_sizes': leak_sizes,
        'water_loss_estimates': water_loss_estimates
    }

    return render_template('leak_results.html', result=result)

