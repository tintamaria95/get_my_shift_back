from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_models import Base
from dauphineAPI import get_phpsessid, register_or_unregister_to_shift
from db_functions import get_bookings, get_bookings_for_user, get_user_by_id
from utils import set_course_programme


def main(verbosity=False):
    engine = create_engine("sqlite:///data.db", echo=True)
    Base.metadata.create_all(engine)

    session = Session(engine)

    bookings = get_bookings(session)
    for user_id in bookings.keys():
        bookings_for_user = get_bookings_for_user(session, user_id)
        user = get_user_by_id(session, user_id)
        mail = user["mail"]
        password = user["password"]
        formation = user["formation"]
        phpsessid = get_phpsessid(mail, password)
        for day_booked in bookings_for_user:
            course_programme = set_course_programme(day_booked)
            session_course = "2022MY1LCLIMBU          22010001"
            if verbosity:
                print("phpsessid", phpsessid)
                print("formation", formation)
                print("course_prog", course_programme)
                print("session_course", session_course)
            data = register_or_unregister_to_shift(
                phpsessid=phpsessid,
                user_formation=formation,
                course_program=course_programme,
                session_course=session_course
            )
            value_to_check_regis = str(data).split('"INS":')[1][:4]
            if value_to_check_regis == 'null':
                print(
                    f"FAIL - Un/Registration didn't succeed for user={user_id}"
                    f", day={day_booked}")
            else:
                print(
                    f"SUCCESS - Un/Registration succeed for user={user_id}"
                    f", day={day_booked}")


if __name__ == "__main__":
    main()
