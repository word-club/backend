import os
import datetime
from django.utils.timezone import utc


def get_time_diff_in_days(time_posted):
    if time_posted:
        current = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = current - time_posted
        return int(diff.days)
    return 0


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
