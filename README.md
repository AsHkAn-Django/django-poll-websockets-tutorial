# Polling App With Realtime Response(Sockets)

Just a quick little project I made while practicing Django and backend development.  
This is part of my journey as I learn and improve my skills.

This is a real-time polling application built with Django and Django Channels. It allows users to vote on a poll, and the results are updated instantly across all connected clients using WebSockets.

## Features
- Live vote count updates without page reloads
- WebSocket integration using Django Channels
- Responsive and interactive front-end
- Built with real-time performance in mind

## Technologies Used
- Django
- Django Channels
- WebSockets
- HTML, CSS, JavaScript

## Learning Goals
- Understand and implement asynchronous communication in Django
- Integrate WebSockets for real-time data streaming
- Build dynamic, real-time web applications

## About the Project

This project is built using Django and includes basic frontend styling with HTML, CSS, Bootstrap, and some JavaScript.  
I usually focus on the backend side of things and try to keep things simple and clean.  
Each project I make is a way for me to learn something new or reinforce what I already know.


## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript

## About Me

Hi, I'm Ashkan — a junior Django developer who recently transitioned from teaching English as a second language to learning backend development.  
I’m currently focused on improving my skills, building projects, and looking for opportunities to work as a backend developer.  
You can find more of my work here: [My GitHub](https://github.com/AsHkAn-Django)

## How to Use

1. Clone the repository  
   `git clone https://github.com/AsHkAn-Django/django-poll-websockets-tutorial.git`
2. Navigate into the folder  
   `cd django-poll-websockets-tutorial`
3. Create a virtual environment and activate it
4. Install the dependencies  
   `pip install -r requirements.txt`
5. Run the server  
   `python manage.py runserver`

## Tutorial 


# ✅ Django Channels + WebSockets Setup Checklist

1. Install Requirements

```bash
pip install channels
# Optional (for dev/test):
pip install channels_redis
```

2. Update settings.py
```python
# Enable ASGI
ASGI_APPLICATION = 'your_project_name.asgi.application'

# Optional: Redis layer (for production or multiple workers)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # use RedisChannelLayer for production
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {"hosts": [("127.0.0.1", 6379)]}
    },
}
```

3. Create asgi.py
In your project root (beside settings.py):

```python
# your_project/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import your_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            your_app.routing.websocket_urlpatterns
        )
    ),
})
```

4. Create routing.py in your app

```python
# your_app/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/some_path/(?P<some_id>\d+)/$', consumers.YourConsumer.as_asgi()),
]
```

5. Create the WebSocket Consumer
```python
# your_app/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f'some_group_{self.scope["url_route"]["kwargs"]["some_id"]}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        # Optional: receive data from frontend
        pass

    async def some_update(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
        }))
```

6. Trigger Events from Django Views
```python
# views.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse

def your_view(request, some_id):
    # Your logic here
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'some_group_{some_id}',
        {
            'type': 'some_update',  # Must match method name in consumer
            'message': 'Updated!'
        }
    )
    return HttpResponse("Sent!")

```

7. Frontend JavaScript WebSocket
```html
<script>
    const id = "{{ some_id }}";
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/some_path/${id}/`);

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        document.getElementById('message').innerText = data.message;
    };
</script>
```

8. Run Your App with Daphne or Uvicorn
```bash
# Not manage.py runserver
daphne -b 127.0.0.1 -p 8000 your_project.asgi:application
```

