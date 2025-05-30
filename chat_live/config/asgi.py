"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter#permet de router en fonction du protocole (HTTP ou websocket)
from django.core.asgi import get_asgi_application#permet de gérer HTTP en plus des websocket
from channels.auth import AuthMiddlewareStack#gère l'authentification des utilisateurs sur les websockets
import chatmessage.routing#import routing.py où on a définit les URLs des websocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')#définit la variable d'environnement

print("==> asgi.py module loaded")

#application = get_asgi_application()
#création d'une variable "application", reconnue et cherchée par le serveur (Daphne, Uvicorn...) pour gérer les connexions
#ProtocoleTypeRouter est un objet fournis pas channels, qui détecte le type de connexion (HTTP ou websocket) pour la rediriger
application = ProtocolTypeRouter({
	"http" : get_asgi_application(),#http est redirigé vers asgi
	"websocket" : AuthMiddlewareStack(#websocket passe par middleware qui gère l'authentification
		URLRouter(#puis par un routeur qui va utiliser la liste de route dans routing.py pour envoyer la connexion au bon consummer (=view)
			chatmessage.routing.websocket_urlpatterns
		)
	),
})
