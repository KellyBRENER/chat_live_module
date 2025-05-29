import json
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
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):#self représente l'instance de cette classe (= this)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]#self.scope donne accès aux infos de l'utilisateur
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
