from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatGroup(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chat_groups')

    def __str__(self):
        return self.name if self.name else f"ChatGroup {self.id}"


class Message(models.Model):
    group = models.ForeignKey("ChatGroup", on_delete=models.CASCADE, related_name='messages', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.sender.username}: {self.content[:30]}"
