import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poll_id = self.scope['url_route']['kwargs']['poll_id']
        self.poll_group_name = f'poll_{self.poll_id}'
        print(f"[WS] Connecting to group {self.poll_group_name}")    # ← log

        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Example: broadcast vote update to group
        await self.channel_layer.group_send(
            self.poll_group_name,
            {
                'type': 'vote_update',
                'num_votes': data['num_votes']
            }
        )

    async def vote_update(self, event):
        await self.send(text_data=json.dumps({
            'num_votes': event['num_votes']
        }))
