from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message
import json
import time
from django.http import StreamingHttpResponse
from django.views.decorators.http import condition
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

# Buffer global (simplifié pour test)
latest_messages = []


#à remettre après les tests
@csrf_exempt  # désactive la sécu par défaut de django qui protège des falsifications de requêtes
# @login_required
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("as")
            sender = User.objects.get_or_create(username=username)[0]
            content = data.get("content")
			 # essayer de récupérer recipient si donné
            recipient_username = data.get("recipient")
            if recipient_username:
                recipient = User.objects.get_or_create(username=recipient_username)[0]
            else:
                recipient = None  # message public
            message = Message.objects.create(sender=sender, recipient=recipient, content=content)
            # Ajouter au buffer SSE
            latest_messages.append({
                "sender": sender.username,
                "recipient": recipient.username if recipient else "Tous",
                "content": content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
            return JsonResponse({
                "status": "success",
                "sender": sender.username,
                "recipient": recipient.username if recipient else None,
                "content": content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "POST only"}, status=405)

# @login_required
def chat_page(request):
    return render(request, "chatMessage/chat.html")

# @login_required
def sse_view(request):
    def event_stream():
        last_index = 0
        while True:
            if len(latest_messages) > last_index:
                new = latest_messages[last_index]
                last_index += 1
                yield f"data: {json.dumps(new)}\n\n"
            time.sleep(1)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
