from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask, request

from src.db_models import Base, User
from src.db_functions import unregister, register
from src.db_functions import get_bookings, get_bookings_for_user
from src.env import AuthID

app = Flask(__name__)

engine = create_engine("sqlite:///data.db", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

# Add admin user
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

# # Add climbing day to user
# stmt = select(User).where(User.id == 2)
# martinld = session.scalars(stmt).one()
# martinld.user_climbing_days.append(UserClimbingDay(
#     climbing_day="monday"))
# session.commit()


@app.route("/", methods=["GET"])
def get_all_bookings():
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