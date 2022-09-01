import json
from datetime import datetime

from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from .models import Chat, Message


users = {}
tick = 0

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = str(self.scope["url_route"]["kwargs"]["pk"])
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type_ = text_data_json["type"]
        message = text_data_json["message"]
        if text_data_json["type"] == "user_connect":

            username = text_data_json["username"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": type_, "username": username, "message": message},
            )
        if text_data_json["type"] == "chat_message":
            is_from_search = text_data_json["is_from_search"]
            companion_online = text_data_json["companion_online"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": type_,
                    "message": message,
                    "username": self.scope["user"].username,
                    "time": datetime.now().strftime("%H:%M"),
                    "is_from_search": is_from_search,
                    "companion_online": companion_online,
                    "companion": text_data_json["companion"],
                },
            )

    def create_chat(self, is_from_search, companion):
        if is_from_search:
            current_user = self.scope["user"]
            companion = User.objects.get(username=companion)
            self.chat = Chat.objects.create()
            self.chat.participants.set([current_user, companion])
        else:
            self.chat = Chat.objects.get(id=self.room_name)
            self.companion = self.chat.participants.exclude(
                username=self.scope["user"].username
            )

    def chat_message(self, event):
        global tick
        tick += 1
        is_from_search = event["is_from_search"]
        message = event["message"]
        username = event["username"]
        time = event["time"]
        companion_online = event["companion_online"]
        self.create_chat(is_from_search, event["companion"])
        self.send(
            text_data=json.dumps(
                {
                    "text": message,
                    "sender": username,
                    "time": time,
                    "chat_id": self.chat.id,
                }
            )
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chats",
            {
                "type": "sidebar_chats",
                "text": message,
                "sender": username,
                "time": time,
                "chat_id": self.chat.id,
            },
        )
        if tick == 1:
            user = User.objects.get(username=username)
            message = Message.objects.create(sender=user, text=message)
            if companion_online:
                message.readed = True
                message.save()
            self.chat.messages.add(message)
        if tick > 1:
            tick = 0


    def user_connect(self, event):
        username = event["username"]
        if event["message"] == "disconnect":
            print("remove", event["username"])
            try:
                users[self.room_group_name].remove(username)
            except ValueError:
                print("user already removed")
        else:
            if users.get(self.room_group_name) is None:
                users[self.room_group_name] = []
                users[self.room_group_name].append(username)
            elif username not in users[self.room_group_name]:
                users[self.room_group_name].append(username)
        self.send(text_data=json.dumps({"online": users[self.room_group_name]}))


class UpdateChatsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "chats"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def sidebar_chats(self, event):
        message = event["text"]
        username = event["sender"]
        time = event["time"]
        chat_id = event["chat_id"]
        self.send(
            text_data=json.dumps(
                {
                    "text": message,
                    "username": username,
                    "time": time,
                    "chat_id": chat_id,
                }
            )
        )
