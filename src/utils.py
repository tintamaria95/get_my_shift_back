from datetime import datetime as date
from datetime import timedelta


def get_weekday(day: str):
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
        ]
    return days.index(day) + 1


def get_next_dayofweek_datetime(date_time: date, dayofweek: int):
    start_time_w = date_time.isoweekday()
    target_w = get_weekday(dayofweek)
    if start_time_w < target_w:
        day_diff = target_w - start_time_w
    else:
        day_diff = 7 - (start_time_w - target_w)

    return date_time + timedelta(days=day_diff)


def get_week_number():
    return date.today().isocalendar().week


def set_course_programme(day: str):
    # c = "MY1LCLIMBU220001    SPORT     .   2023-15     Samedi  08:0009:00"
    day = day.lower()
    day_mapping = {
        "monday": "Lundi   ",
        "tuesday": "Mardi   ",
        "wednesday": "Mercredi",
        "thursday": "Jeudi   ",
        "friday": "Vendredi",
        "saturday": "Samedi  ",
        "sunday": "Dimanche"}
    year = get_next_dayofweek_datetime(date.today(), day)
    week = get_week_number()
    course_programme = (
        f"MY1LCLIMBU220001    SPORT     .   {str(year)[:4]}-{week}"
        f"     {day_mapping[day]}08:0009:00")
    return course_programme


if __name__ == "__main__":
    print("Example: Date of next sunday ->")
    dtemp = get_next_dayofweek_datetime(date.today(), 'sunday')
    print(str(dtemp)[:7])
