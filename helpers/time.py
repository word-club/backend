import datetime
from django.utils import timezone


now = timezone.now()
today = datetime.datetime.today()

today_first_clock = now.replace(hour=0, minute=0, second=0, microsecond=0)

before_three_days = today - datetime.timedelta(days=3)
before_three_days = now.replace(
    year=before_three_days.year,
    month=before_three_days.month,
    day=before_three_days.day,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
)

first_day_of_week = today - datetime.timedelta(days=today.isoweekday() % 7)
first_day_of_week = now.replace(
    year=first_day_of_week.year,
    month=first_day_of_week.month,
    day=first_day_of_week.day,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
)
