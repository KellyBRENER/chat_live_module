from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')

admin.site.register(ChatMessage, ChatMessageAdmin)
