from django.shortcuts import render

# Create your views here.
print("==> views.py module loaded")

def chat_view(request):
    return render(request, "chatmessage/chat.html")
