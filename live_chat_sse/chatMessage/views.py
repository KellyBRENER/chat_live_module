from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message, ChatGroup
import json
import time
from django.views.decorators.http import condition
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now, timedelta

# Create your views here.

#à remettre après les tests
@csrf_exempt  # désactive la sécu par défaut de django qui protège des falsifications de requêtes
# @login_required
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
            return JsonResponse({
                "status": "success",
                "sender": sender.username,
                "group": group.name,
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
    group_name = request.GET.get("group", "general")
    if not group_name:
        return StreamingHttpResponse("Missing group ID", status=400)
    group = get_object_or_404(ChatGroup, name=group_name)
    def event_stream():
        last_message_id = 0
        while True:
            new_messages = Message.objects.filter(
                group=group,
                id__gt=last_message_id
                ).order_by("timestamp")

            for msg in new_messages:
                msg_data = {
                    "sender": msg.sender.username,
                    "content": msg.content,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    }
                last_message_id = msg.id
                yield f"data: {json.dumps(msg_data)}\n\n"
            time.sleep(1)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
