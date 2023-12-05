def add_pipe(db):
    from .models import Pipe
    new_pipe = Pipe(
        start_point="Water Treatment Plant",
        end_point="Residential Area A",
        diameter=12,
        water_pressure=70.0,
        length=2500
    )
    
    new_pipe2 = Pipe(
        start_point="Industrial Zone E",
        end_point="Commercial Area F",
        diameter=8,
        water_pressure=60.0,
        length=2800
    )
    
    new_pipe3 = Pipe(
        start_point="Pumping Station C",
        end_point="Suburb D",
        diameter=6,
        water_pressure=66.0,
        length=3500
    )
    new_pipe4 = Pipe(
    start_point="Reservoir X",
    end_point="Industrial Zone Y",
    diameter=10,
    water_pressure=55.0,
    length=3000
    )

    new_pipe5 = Pipe(
        start_point="Commercial Area Z",
        end_point="Residential Area W",
        diameter=14,
        water_pressure=75.0,
        length=1800
    )

    new_pipe6 = Pipe(
        start_point="Water Source P",
        end_point="Suburb Q",
        diameter=8,
        water_pressure=62.0,
        length=2000
    )

    new_pipe7 = Pipe(
        start_point="Municipal Pumping Station",
        end_point="Public Park R",
        diameter=16,
        water_pressure=80.0,
        length=3500
    )

    db.session.add(new_pipe)
    db.session.add(new_pipe2)
    db.session.add(new_pipe3)
    db.session.add(new_pipe4)
    db.session.add(new_pipe5)
    db.session.add(new_pipe6)
    db.session.add(new_pipe7)
    db.session.commit()
def add_device(db):
    from .models import Device
    from .models import Device

    new_device2 = Device(
        model="Pressure Monitor A",
        diameter=0.8
    )

    new_device3 = Device(
        model="Pressure Monitor B",
        diameter=0.4 
    )

    new_device4 = Device(
        model="Pressure Monitor C",
        diameter=0.6 
    )

    db.session.add(new_device2)
    db.session.add(new_device3)
    db.session.add(new_device4)
    db.session.commit()
    print("device added!")
def add_user(db):
    from werkzeug.security import generate_password_hash
    from .models import User

    email = "mariam@wlds.ae"
    password1 = "1234567"
    first_name = "mariam"
    email2 = "Dr.Manar@wlds.ae"
    password2 = "1234567"
    first_name2 = "Dr.Manar"
    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))

        try:
            db.session.add(new_user)
            db.session.commit()
            print('User added successfully!')
        except Exception as e:
            print(f'Error adding user: {e}')
    user2 = User.query.filter_by(email=email2).first()           
    if not user2:
        new_user2 = User(email=email2, first_name=first_name2, password=generate_password_hash(password2))

        try:
            db.session.add(new_user2)
            db.session.commit()
            print('User added successfully!')
        except Exception as e:
            print(f'Error adding user: {e}')