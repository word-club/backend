from django.core.exceptions import ValidationError


def validate_unique_id(value):
    items_to_ignore = ["\\", " ", "#", "?", "/", "&", "^", "%", "@", "!"]
    for item in items_to_ignore:
        if item in value:
            raise ValidationError(", ".join(items_to_ignore) + " are not allowed.")
