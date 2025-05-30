import json #pour encoder / décoder les messages en format json
from channels.generic.websocket import AsyncWebsocketConsumer


#la classe doit hérité d'un des consumers de django channels:
#-> AsyncWebsocketConsumer = gère les événements des websocket
#		- async def : permet d'attendre des choses sans bloquer le programme
#-> WebsocketConsumer = version synchrone des websocket (utilise def au lieu de async def)
#-> AsyncConsumer / SyncConsumer
#la classe doit implémenter certaines méthodes spécifiques:
#- connect(self) : quand un client se connecte (puis self.accept() pour autoriser la connection)
#- receive(self, text_data) : quand un message est reçu
#- disconnect(self, close_code): quand la connection se ferme

print("==> consumers.py module loaded")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):#connect est appelé automatiquementqd un client se connecte (self = this)
        print("Connect called")
        print("channel_layer:", self.channel_layer)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]#crée la variable room_name dans self et y stock la valeur de room_name récupéré dans routing.py // self.scope donne accès aux infos de l'utilisateur
        self.room_group_name = f"chat_{self.room_name}"#crée le groupe "room_group_name" à partir de "room_name"
        # Join room group
        await self.channel_layer.group_add(#ajoute la websocket "channel_name" au groupe "room_group_name"
            self.room_group_name,
            self.channel_name
        )
#await attend que l'action soit faite sans bloquer le programme, à utiliser dans async def
        await self.accept()#accept la connexion

    async def disconnect(self, close_code):#close_code = raison de la fermeture
        # Leave room group
        await self.channel_layer.group_discard(#enlève cette socket du groupe
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):#appelé automatiquement à chaque fois que le client envoie un message
        print("Message reçu:", text_data)
        data = json.loads(text_data)#convertit le text en dico python
        message = data["message"]#on récupére le message

        # Send message to room group
        await self.channel_layer.group_send(#on envoit le message à tout le groupe
            self.room_group_name,
            {
                "type": "chat_message",#appel de la fonction "chat_message"
                "message": message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]#récupére le message

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))

#ce que contient self.scope:
# {
#     'type': 'websocket',
#     'path': '/ws/chat/general/',
#     'raw_path': b'/ws/chat/general/',
#     'headers': [
#         (b'host', b'localhost:8000'),
#         (b'upgrade', b'websocket'),
#         (b'connection', b'Upgrade'),
#         (b'sec-websocket-key', b'xyz=='),
#         # ...
#     ],
#     'query_string': b'',
#     'client': ['127.0.0.1', 54321],
#     'server': ['127.0.0.1', 8000],
#     'subprotocols': [],
#     'asgi': {
#         'version': '3.0',
#         'spec_version': '2.1'
#     },
#     'url_route': {
#         'args': (),//variables stockées dynamiquement via routing.py
#         'kwargs': {//dictionnaire pour stocker des variables nommées créées dynamiquement dans routing.py
#             'room_name': 'general'
#         }
#     },
#     'user': <AnonymousUser>,
#     'session': <django.contrib.sessions.backends.db.SessionStore object at 0x...>
# }
