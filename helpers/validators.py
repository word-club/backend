from django.utils import timezone

now = timezone.now()


def validate_date_string(value, upto_month=False, year_only=False, to=False):
    if not year_only:
        if "/" in value:
            value = value.split("/")
        elif "-" in value:
            value = value.split("-")
        else:
            return False, "Please use / or - as the separators."
        if upto_month:
            if len(value) != 2:
                return (
                    False,
                    "Please use year then month order for date string in format YYYY-MM. Ex: 2020-02",
                )
            value = now.replace(
                year=int(value[0]),
                month=int(value[1]),
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        else:
            if len(value) != 3:
                return (
                    False,
                    "Please user year, month and month order for date string in format YYYY-MM-DD. Ex: 2020-02-20",
                )
            if not to:
                value = now.replace(
                    year=int(value[0]),
                    month=int(value[1]),
                    day=int(value[2]),
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
            else:
                value = now.replace(
                    year=int(value[0]),
                    month=int(value[1]),
                    day=int(value[2]),
                    hour=23,
                    minute=59,
                    second=59,
                    microsecond=999999,
                )
    else:
        import re

        regexp = re.compile(r"^\d{4}$")
        if not regexp.search(value):
            return False, "Please use 4 digit year string in format YYYY. Ex: 2020"
        else:
            value = now.replace(
                year=int(value),
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

    if value > now:
        return False, "Please use past dates only for filtration."
    return value, None


def check_sort_by_query(sort_by):
    if not sort_by:
        return "support"
    else:
        if sort_by in ["support", "popularity", "discussions", "unix"]:
            return "support"
        return sort_by


def check_bool_query(value):
    try:
        return bool(int(value)) if value else False
    except ValueError:
        return False
