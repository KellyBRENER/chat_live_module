from django.urls import re_path
from . import consumers

#liste d'URL de websocket que django utilisera
print("==> routing.py module loaded")

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
#re_path = path mais accepte des expressions regulieres. les parametres = une string pour le path + un consumer
#r = raw string = n'interprete pas les \
#ws = prefixe pour websocket, c'est a definir personnellement
#\w+ = au moins un (+) caractere alphanumerique (\w)
#/$ = l'url doit finir pr / et $ signifie fin de la chaine
#ChatConsumer = une classe dans consumer.py
#as_asgi() = methode de django channels qui transforme la classe ChatConsumer en "application asgi"
#c'est a dire utilisable par django pour qu'il puisse lui transmettre les messages
#pour qu'une classe puisse etre transformee en appli asgi, il faut qu'elle suive une certaine structure
#voir details dans consumers.py
