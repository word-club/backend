from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("broadcast", self.channel_name)
        print("Added {} channel to broadcast".format(self.channel_name))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("broadcast", self.channel_name)
        print("Removed {} channel from broadcast".format(self.channel_name))

    async def broadcast_notification(self, event):
        await self.send_json(event)
