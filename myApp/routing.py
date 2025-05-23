from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    r"^ws/poll/(?P<poll_id>\d+)/$",         # captures poll_id from the URL
    consumers.PollConsumer.as_asgi()         # the consumer that handles it
]
