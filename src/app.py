from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask, request, current_app

from src.db_models import Base, User
from src.db_functions import unregister, register
from src.db_functions import get_bookings, get_bookings_for_user, get_users
from src.env import AuthID

app = Flask(__name__)

engine = create_engine("sqlite:///data.db", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

# Add admin user if no user in db
if len(session.query(User).all()) == 0:
    martinld = User(
        id=1,
        firstname='Martin',
        lastname='LE DIGABEL',
        mail=AuthID['mail'],
        password=AuthID['password']
    )
    session.add_all([martinld])
    session.commit()

# app.static_folder = Path(app.root_path, Path("/static"))
print(app.static_url_path)
print(app.static_folder)


@app.route("/")
def show_api():
    return current_app.send_static_file("home.html")


@app.route("/bookings", methods=["GET"])
def show_bookings():
    bookings = get_bookings(session)
    return bookings


@app.route("/", methods=["POST"])
def post_users():
    body = request.get_json()
    user_id = body["id"]
    day_to_change_status = body["day"]
    booked_days = get_bookings_for_user(session, user_id)

    if day_to_change_status in booked_days:
        unregister(session, user_id, day_to_change_status)
    else:
        register(session, user_id, day_to_change_status)
    return {"success": True}


@app.route("/users", methods=["GET"])
def show_users():
    return get_users(session)
