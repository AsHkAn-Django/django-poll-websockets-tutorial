import os, django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import myApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poll.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),           # normal HTTP
    "websocket": AuthMiddlewareStack(         # WebSockets get routed here
        URLRouter(
            myApp.routing.websocket_urlpatterns
        )
    ),
})
