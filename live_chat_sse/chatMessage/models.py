# chatMessage/models.py

from django.db import models
from django.contrib.auth.models import User # Ou votre modèle d'utilisateur personnalisé

class ChatGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_private = models.BooleanField(default=False)
    # Ajouter un ManyToManyField pour les membres afin de faciliter la requête des chats privés
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} dans {self.group.name}: {self.content[:50]}"

    class Meta:
        ordering = ['timestamp'] # Assurer que les messages sont triés par horodatage par défaut
