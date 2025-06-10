# chatMessage/views.py

import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message, ChatGroup

# Intégration de Channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@csrf_exempt
# @login_required # Décommentez lorsque l'authentification est prête
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            sender = User.objects.get_or_create(username=username)[0]
            content = data.get("content")
            group_name = data.get("group_name")
            group, _ = ChatGroup.objects.get_or_create(name=group_name)

            message = Message.objects.create(sender=sender, group=group, content=content)

            # --- Notification Channels ---
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group_name, # Nom du groupe (par exemple, 'general' ou 'private_utilisateur1_utilisateur2')
                {
                    "type": "chat_message", # Nom de la méthode dans le consommateur (chat_message)
                    "message": {
                        "sender": sender.username,
                        "sender_id": sender.id,
                        "content": content,
                        "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "group_name": group_name, # Envoyer aussi le nom du groupe au frontend
                    },
                },
            )
            # --- Fin Notification Channels ---

            return JsonResponse({
                "status": "success",
                "sender": sender.username,
                "sender_id": sender.id,
                "group": group.name,
                "content": content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "POST only"}, status=405)

@csrf_exempt
# @login_required # Décommentez lorsque l'authentification est prête
def create_or_get_private_group(request):
    if request.method == 'POST':
        current_username = request.POST.get('current_username')
        target_username = request.POST.get('target_username')

        if not current_username or not target_username:
            return JsonResponse({'error': 'Missing current_username or target_username'}, status=400)

        current_user = User.objects.get_or_create(username=current_username)[0]
        target_user = User.objects.get_or_create(username=target_username)[0]

        user_usernames = sorted([current_user.username, target_user.username])
        group_name = f'private_{user_usernames[0]}_{user_usernames[1]}'

        try:
            group, created = ChatGroup.objects.get_or_create(
                name=group_name,
                defaults={'is_private': True}
            )

            # Ajouter les membres au groupe (en utilisant le ManyToManyField)
            group.members.add(current_user, target_user)

            return JsonResponse({'group_name': group.name, 'created': created})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# @login_required # Décommentez lorsque l'authentification est prête
def chat_page(request):
    # Cette vue ne fera désormais que rendre la page HTML.
    # La messagerie en temps réel sera gérée par les WebSockets.
    return render(request, "chatMessage/chat.html")
