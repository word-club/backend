import os
import random


def get_upload_path(instance, filename, mode):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    upload_to = ""
    if instance.__class__.__name__ == "Image":
        if instance.publication:
            upload_to = f"publications/{instance.publication.id}/"
        elif instance.comment:
            upload_to = f"publications/{instance.comment.id}/"
    elif instance.profile:
        upload_to += f"profile/{instance.profile.created_by.username}/"
    elif instance.community:
        upload_to += f"community/{instance.community.id}/"
    upload_to += f"{mode}/{filename}"
    return upload_to


def upload_avatar_to(instance, filename):
    return get_upload_path(instance, filename, "avatar")


def upload_cover_to(instance, filename):
    return get_upload_path(instance, filename, "cover")


def upload_image_to(instance, filename):
    return get_upload_path(instance, filename, "image")
