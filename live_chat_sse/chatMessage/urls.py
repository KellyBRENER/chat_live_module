from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
	path('stream/', views.sse_view, name='sse'),
	path('', views.chat_page, name='chat_page'),
]
