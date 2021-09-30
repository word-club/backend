import datetime
import os

from django.utils.timezone import utc


def generate_url_for_media_resource(media_url):
    http = "https" if os.getenv("IS_SECURE") else "http"
    base_url = os.getenv("BASE_URL")
    return "{}://{}{}".format(http, base_url, media_url)


def get_time_diff_in_days(time_posted):
    if time_posted:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = now - time_posted
        return int(diff.days)
    return 0
