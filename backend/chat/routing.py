from django.urls import path

from .consumers import ChatConsumer, UpdateChatsConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:pk>/", ChatConsumer.as_asgi()),
    path("ws/chats/", UpdateChatsConsumer.as_asgi()),
]
