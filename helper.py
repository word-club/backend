import os


def generate_url_for_media_resource(media_url):
    http = "https" if os.getenv("IS_SECURE") else "http"
    base_url = os.getenv("BASE_URL")
    return "{}://{}{}".format(http, base_url, media_url)
