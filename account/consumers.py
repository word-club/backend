from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer


class LoginConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("broadcast", self.channel_name)
        print(f"Added {self.channel_name} channel to the group 'broadcast'")
        self.send_json({"message": "Connected to the broadcast group"})

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("broadcast", self.channel_name)
        print(f"Removed {self.channel_name} channel from the group broadcast")
