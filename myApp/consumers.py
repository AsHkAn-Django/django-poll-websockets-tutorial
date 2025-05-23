import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1) Retrieve poll_id from URL
        self.poll_id = self.scope['url_route']['kwargs']['poll_id']
        # 2) Build a group name (all sockets for the same poll share a group)
        self.poll_group_name = f'poll_{self.poll_id}'
        
        # 3) Join that group
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )
        
        # 4) Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group on disconnect
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


    # This handler is invoked when you do group_send(type="vote_update", …)
    async def vote_update(self, event):
        # event = {"type": "vote_update", "num_votes": X}
        await self.send(text_data=json.dumps({
            'num_votes': event['num_votes']
        }))
