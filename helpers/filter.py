from .time import *


def fetch_query(request):
    publication = request.query_params.get("publication", None)  # expects pk
    community = request.query_params.get("community", None)  # expects pk

    all_time = check_bool_query(request.query_params.get("all_time", None))  # expects 0|1
    q_today = check_bool_query(request.query_params.get("today", None))  # expects 0|1
    this_week = check_bool_query(request.query_params.get("this_week", None))  # expects 0|1

    from_query = request.query_params.get("from", None)  # expects date string
    to_query = request.query_params.get("to", None)  # expects date string
    year = request.query_params.get("year", None)  # expects year
    month = request.query_params.get("month", None)  # expects month number
    day = request.query_params.get("day", None)  # expects day number

    search = request.query_params.get("search", None)  # expects plain string

    return {
        "publication": publication,
        "community": community,
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


def get_user_from_auth_header(request):
    auth_header = request.headers.get("Authorization", False)
    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            token_instance = Token.objects.get(key=token)
            return token_instance.user
        except Token.DoesNotExist:
            return None
    else:
        return None


def get_viewset_filterset(request, filterset_fields, default_field):
    if Administration.objects.count() == 0:
        Administration.objects.create()
    pt = Administration.objects.first().popularity_threshold

    # for public users set popularity threshold for every filterset
    requestor = get_user_from_auth_header(request)
    threshold = 0 if requestor else pt

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
            if item in ["publication", "created_by", "community", "reply"]:
                value = int(value)
            filterset[item] = value
    sort_string = "-{}".format(default_field)
    if sort_by in ["popularity", "supports", "discussions", "views"]:
        filterset["{}__gte".format(sort_by)] = threshold
        sort_string = "{}{}".format("-" if not asc else "", sort_by)
    if sort_by in ["{}".format(default_field)]:
        filterset["popularity__gte"] = threshold

    search = request.query_params.get("search")
    search_by = request.query_params.get("search_by")
    if search and search_by:
        filterset["{}__contains".format(search_by)] = search

    return filterset, sort_string
