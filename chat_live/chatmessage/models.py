from django.db import models

# Create your models here.

class ChatMessage(models.Model):#creation d'une class "chatmessage" qui herite de la classe Model de Django
	sender = models.CharField(max_length=100)#definit une chaine de carac nommee sender
	recipient = models.CharField(max_length=100)
	content = models.TextField()#definit un champ pour des textes longs
	timestamp = models.DateTimeField(auto_now_add=True)#champ pour stocker date et heure au format DATETIME, ajoute automatiquement date et heure actuelle

