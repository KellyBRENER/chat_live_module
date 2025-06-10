# chatMessage/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, ChatGroup
from django.utils.timezone import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Le nom du groupe provient de l'URL (par exemple, /ws/chat/<nom_du_groupe>/)
        # Nous utiliserons le nom du groupe directement comme nom de groupe de canaux pour simplifier
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        # Ajouter le consommateur au groupe
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Envoyer les messages existants lors de la connexion
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps(message))

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Recevoir un message du WebSocket
    async def receive(self, text_data):
        # Ce consommateur sert principalement à envoyer des messages DU serveur au client.
        # Les messages du client sont généralement gérés par une requête HTTP POST séparée
        # (votre vue send_message existante) qui enregistre ensuite le message dans la base de données
        # et notifie Channels.
        # Cependant, pour une fonctionnalité WebSocket complète, vous pourriez aussi gérer les messages
        # envoyés par le client ici.
        pass

    # Recevoir un message de la couche de canal (depuis la vue send_message ou un autre consommateur)
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @sync_to_async
    def get_messages(self):
        # Récupérer les N derniers messages pour le groupe
        try:
            group = ChatGroup.objects.get(name=self.group_name)
            messages = Message.objects.filter(group=group).order_by('timestamp')[:50] # Les 50 derniers messages
            return [{
                "sender": msg.sender.username,
                "sender_id": msg.sender.id,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            } for msg in messages]
        except ChatGroup.DoesNotExist:
            return []
