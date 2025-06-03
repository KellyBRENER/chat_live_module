#classe de base qui crée des tables dans la base de données (fiat les requete sql pour nous)
from django.db import models
#modèle User fourni par django, chaque utilisateur est une instance de cette classe
from django.contrib.auth.models import User
#pour récupérer l'heure actuel
from django.utils import timezone

# Create your models here.
#crée une classe "message" qui sera considérée comme une table dans la db
#un attribut = une colonne
class	Message(models.Model):
	#récupère le lien vers l'id de l'utilisateur qui envoie le message
	#donc on doit faire le lien avec la table user dans la db (contient id, username, email ...)
	#crée une colonne sender_id dans la table message
	#sender_id pointe vers la colonne id de la table User qui permettra de récupérer des infos si besoin
	#si l'id du User est supprimé dans la table User, on supprime tous ses messages
	#related_name sert à nommer la colonne "messages envoyés" dans User par 'sent_message'
	#dans la table user on pourra ainsi récupéré tous les messages envoyés par ce user
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
	content = models.TextField()#texte du message sans taille limite
	timestamp = models.DateTimeField(default=timezone.now)#récupère la date et l'heure actuelle

#affichage lisible dans l'admin ou en debug
#méth python qui définit ce qu'on voit quand on utilise print()
	def __str__(self):
		return f'{self.sender.username}: {self.content[:20]}'
