# chatMessage/routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<group_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # Nous utiliserons ce chemin pour les mises à jour en temps réel de type SSE.
    # Note : EventSource attend un point de terminaison HTTP standard, pas un WebSocket.
    # Nous adapterons ChatConsumer pour envoyer des trames de données régulières sur le WebSocket,
    # et le frontend utilisera une connexion WebSocket au lieu d'EventSource.
    # Pour un *vrai* SSE avec Channels, vous définiriez un `AsgiHttpConsumer` séparé ou similaire,
    # mais les WebSockets sont généralement préférés pour un chat bidirectionnel.
]
