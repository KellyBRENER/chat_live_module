import os
import django # <--- Add this import

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Set the Django settings module environment variable FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_chat_sse.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application() # This calls django.setup() internally

# Now you can import your application-specific routing and consumers
# as Django's environment is fully set up.
import chatMessage.routing # <--- Move this import AFTER get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app, # Use the initialized ASGI application for HTTP
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chatMessage.routing.websocket_urlpatterns
            )
        )
    ),
})
