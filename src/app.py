from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask, request, current_app

from db_models import Base, User
from db_functions import unregister, register
from db_functions import get_bookings, get_bookings_for_user, get_users
from db_functions import signup, delete
from env import AuthID, PORT
from dauphineAPI import get_user_formation

app = Flask(__name__)

engine = create_engine("sqlite:///data.db", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

allowed_days_entries = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
    ]

# Add admin user if no user in db
if len(session.query(User).all()) == 0:
    try:
        martinld = User(
            id=1,
            firstname='Martin',
            lastname='LE DIGABEL',
            mail=AuthID['mail'],
            password=AuthID['password'],
            formation=get_user_formation(AuthID['mail'], AuthID['password'])
        )
        session.add_all([martinld])
        session.commit()
    except ValueError:
        raise ValueError("Couldn't create Auth User")

# app.static_folder = Path(app.root_path, Path("/static"))
print(app.static_url_path)
print(app.static_folder)


@app.route("/")
def show_home():
    return current_app.send_static_file("home.html")


@app.route("/protected")
def show_api():
    return current_app.send_static_file("api.html")


@app.route("/bookings", methods=["GET"])
def show_bookings():
    bookings = get_bookings(session)
    return bookings


@app.route("/", methods=["POST"])
def post_users():
    body = request.get_json()
    user_id = body["id"]
    day_to_change_status = body["day"]
    if day_to_change_status.lower() not in allowed_days_entries:
        print("Log: Specified value value for day not accepted when POST req.")
        return {"success": False}
    else:
        booked_days = get_bookings_for_user(session, user_id)

        if day_to_change_status in booked_days:
            unregister(session, user_id, day_to_change_status)
        else:
            register(session, user_id, day_to_change_status)
    return {"success": True}


@app.route("/users", methods=["GET"])
def show_users():
    return get_users(session)


@app.route("/users/signup", methods=["POST"])
def signup_user():
    body = request.get_json()
    firstname = body["firstname"]
    lastname = body["lastname"]
    mail = body["mail"]
    password = body["password"]
    try:
        signup(
            session=session,
            firstname=firstname,
            lastname=lastname,
            mail=mail,
            password=password
        )
        return {"success": True}
    except ValueError:
        print(f"Unknown User with mail={mail} and pwd={password}")


@app.route("/users/delete", methods=["POST"])
def delete_user():
    body = request.get_json()
    try:
        user_id = int(body["id"])
        delete(
            session=session,
            user_id=user_id
        )
        return {"success": True}
    except ValueError:
        print(f"Unable to delete user with id={user_id}")


if __name__ == "__main__":
    app.run(port=PORT)
