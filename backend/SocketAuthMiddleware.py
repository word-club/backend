from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user_from_token(token):
    try:
        return Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return None


class UserAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        user, token = None, None
        query = scope.get("query_string", b"")
        if query:
            query = query.decode()
            if "=" in query:
                token = query.split("=")[1]
        if token:
            user = await get_user_from_token(token)
        if isinstance(user, get_user_model()):
            scope["user"] = user
        return await self.app(scope, receive, send)
