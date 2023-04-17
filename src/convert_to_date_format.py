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


if __name__ == "__main__":
    print("Example: Date of next sunday ->")
    print(get_next_dayofweek_datetime(date.today(), 'sunday'))
