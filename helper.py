import datetime
import os
import uuid
from collections import OrderedDict

import requests
from django.utils import timezone
from django.utils.timezone import utc
from rest_framework import serializers

# from administration.models import Administration
from backend.settings.base import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from publication.validators import check_bool_query, validate_date_string

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


def generate_url_for_media_resource(media_url):
    http = "https" if os.getenv("IS_SECURE") else "http"
    base_url = os.getenv("BASE_URL")
    return "{}://{}{}".format(http, base_url, media_url)


def get_time_diff_in_days(time_posted):
    if time_posted:
        current = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = current - time_posted
        return int(diff.days)
    return 0


def check_size(resource, max_size):
    """
    Serializer validator
    Validates file size
    Raises serializer validation error if requirement does not match
    """
    if resource.size / 1000 > max_size:
        raise serializers.ValidationError(
            f"Resource exceeds maximum upload size." f" Allowed maximum size: {max_size / 1000} MB"
        )


def check_extension(resource, allowed_extensions_array):
    """
    Serializer Validator
    Validates file extension
    Raises serializer validation error if requirement does not match
    """
    ext = resource.name.split(".")[-1]
    if ext not in allowed_extensions_array:
        raise serializers.ValidationError(
            f"Resource extension '{ext}' is not allowed for upload."
            f" Allowed extensions are: {', '.join(allowed_extensions_array)}"
        )


def check_images_size_with_ext(images):
    for image in images:
        check_extension(image, ALLOWED_IMAGES_EXTENSIONS)
        check_size(image, MAX_UPLOAD_IMAGE_SIZE)


def check_image_size_with_ext(image):
    check_extension(image, ALLOWED_IMAGES_EXTENSIONS)
    check_size(image, MAX_UPLOAD_IMAGE_SIZE)


# reports: list of reports
# compares each report's timestamp
# if a report made withing 15 days is found, returns True
# else returns False
def is_recent_report_present(reports):
    most_recent_report_found = False
    diff = None
    for report in reports:
        diff = get_time_diff_in_days(report.timestamp)
        if diff < 15:
            most_recent_report_found = True
            break
        diff = None
    return most_recent_report_found, diff


def get_twitter_embed_data(source):
    response = requests.get("https://publish.twitter.com/oembed?url={}".format(source))
    return response.json()


def fetch_query(request):
    publication = request.query_params.get("publication")  # expects pk
    all_time = check_bool_query(request.query_params.get("all_time"))  # expects 0|1
    q_today = check_bool_query(request.query_params.get("today"))  # expects 0|1
    this_week = check_bool_query(request.query_params.get("this_week"))  # expects 0|1

    from_query = request.query_params.get("from")  # expects date string
    to_query = request.query_params.get("to")  # expects date string
    year = request.query_params.get("year")  # expects year
    month = request.query_params.get("month")  # expects month number
    day = request.query_params.get("day")  # expects day number

    search = request.query_params.get("search")  # expects plain string

    return {
        "publication": publication,
        "all_time": all_time,
        "today": q_today,
        "this_week": this_week,
        "from_query": from_query,
        "to_query": to_query,
        "year": year,
        "month": month,
        "day": day,
        "search": search if search else False,
    }


def get_filter_range(params):
    from_query = params["from_query"]
    to_query = params["to_query"]
    year = params["year"]
    month = params["month"]
    day = params["day"]
    p_today = params["today"]
    this_week = params["this_week"]

    if from_query and to_query:
        from_date, err = validate_date_string(from_query)
        if err:
            return None, err
        to_date, err = validate_date_string(to_query, to=True)
        if err:
            return None, err
        timestamp_range = [from_date, to_date]

    elif year and month and day:
        date, err = validate_date_string("{}/{}/{}".format(year, month, day))
        if err:
            return None, err
        timestamp_range = [date, now]
    elif year and month:
        date, err = validate_date_string("{}/{}".format(year, month), upto_month=True)
        if err:
            return None, err
        timestamp_range = [date, now]
    elif year:
        date, err = validate_date_string("{}".format(year), year_only=True)
        if err:
            return None, err
        timestamp_range = [date, now]
    elif p_today:
        timestamp_range = [today_first_clock, now]
    elif this_week:
        timestamp_range = [first_day_of_week, now]
    else:
        timestamp_range = [before_three_days, now]
    return timestamp_range, None


def get_viewset_filterset(request, filterset_fields, default_field):
    # TODO: fix this
    # pt = Administration.objects.first().popularity_threshold
    # AttributeError: 'NoneType' object has no attribute 'popularity_threshold'

    # pt = Administration.objects.first().popularity_threshold
    sort_by = request.query_params.get("sort_by")
    asc = request.query_params.get("asc")
    asc = check_bool_query(asc)
    filterset = OrderedDict()
    for item in filterset_fields:
        value = request.query_params.get(item)
        if value:
            if value == "true":
                value = True
            if value == "false":
                value = False
            if item in ["publication", "created_by", "community"]:
                value = int(value)
            if item in ["reply"]:
                value = uuid.UUID(value)
            filterset[item] = value
    sort_string = "-{}".format(default_field)
    if sort_by in ["popularity", "supports", "discussions", "views"]:
        # only view items with reactions more than administration limit
        filterset["{}__gte".format(sort_by)] = 0  # TODO: replace with pt here
        sort_string = "{}{}".format("-" if not asc else "", sort_by)
    # for fresh item sort, only show items with popularity less than administration limit
    if sort_by in ["{}".format(default_field)]:
        filterset["popularity__gt"] = 1  # TODO: replace with pt here

    search = request.query_params.get("search")
    search_by = request.query_params.get("search_by")
    if search and search_by:
        filterset["{}__contains".format(search_by)] = search

    return filterset, sort_string
