from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db_models import User, UserClimbingDay


def get_bookings(session: Session):
    res = session.query(
        User.id, User.firstname, User.lastname, UserClimbingDay.climbing_day)\
        .join(UserClimbingDay, UserClimbingDay.user_id == User.id).all()
    print(res)
    bookings = {}
    for t in res:
        if t[0] not in bookings.keys():
            bookings[t[0]] = {"firstname": t[1], "lastname": t[2],
                              "climbing_days": []}
            if t[3]:
                bookings[t[0]]["climbing_days"].append(t[3])
        else:
            bookings[t[0]]["climbing_days"].append(t[3])
    return bookings


def get_bookings_for_user(session: Session, user_id: int):
    # check if day in bookings
    stmt = (
        select(UserClimbingDay.climbing_day)
        .join(UserClimbingDay.user)
        .where(User.id == user_id)
    )
    booked_days = session.scalars(stmt).all()
    return booked_days


def unregister(session: Session, user_id: int, day: str):
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    stmt = (
        select(UserClimbingDay)
        .join(UserClimbingDay.user)
        .where(User.id == user_id)
        .where(UserClimbingDay.climbing_day == day)
    )
    day_to_remove = session.scalars(stmt).one()
    user.user_climbing_days.remove(day_to_remove)
    session.commit()


def register(session: Session, user_id, day: str):
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    user.user_climbing_days.append(
        UserClimbingDay(climbing_day=day))
    session.commit()