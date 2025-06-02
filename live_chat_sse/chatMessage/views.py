from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message
import json

# Create your views here.
#à remettre après les tests
@csrf_exempt  # désactive la sécu par défaut de django qui protège des falsifications de requêtes
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            username = data.get("username")

            user = User.objects.get(username=username)

            message = Message.objects.create(
                sender=user,
                content=content
            )

            return JsonResponse({"status": "success", "message_id": message.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "POST only"}, status=405)

def chat_page(request):
    return render(request, "chatMessage/chat.html")
