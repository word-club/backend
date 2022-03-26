from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(JsonWebsocketConsumer):
    def get_user_from_scope(self):
        return self.scope.get("user", None)

    def connect(self):
        self.accept()
        user = self.get_user_from_scope()
        if not user:
            self.send_json({"error": "Not authenticated"})
            self.close()
        else:
            async_to_sync(self.channel_layer.group_add)(f"{user.username}", self.channel_name)
            print(f"Added {self.channel_name} channel to the group '{user.username}'")
            self.send_json({"message": f"{user.username} connected to his personal group"})

    def disconnect(self, code):
        user = self.get_user_from_scope()
        if user:
            async_to_sync(self.channel_layer.group_discard)(f"{user.username}", self.channel_name)
            print(f"Removed {self.channel_name} channel from the group '{user.username}'")

    def notify(self, event):
        self.send_json(event)
