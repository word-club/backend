from rest_framework import serializers

from backend.settings.base import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


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
