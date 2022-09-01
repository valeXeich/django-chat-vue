from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username")
    created = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["sender", "text", "readed", "created"]
    
    def get_created(self, obj):
        return obj.created.strftime('%H:%M')


class ChatSerizlizer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ["messages"]


class ChatEnterSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = self.context["request"].user

    companion = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    unreaded_messages = serializers.SerializerMethodField(
        method_name="get_unread_messages"
    )
    current_user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "companion",
            "last_message",
            "time",
            "id",
            "unreaded_messages",
            "current_user",
        ]

    def get_companion(self, obj):
        self.chat_companion = obj.participants.exclude(username=self.user.username)[0]
        return self.chat_companion.username

    def get_last_message(self, obj):
        return obj.messages.latest("created").text

    def get_time(self, obj):
        message = obj.messages.latest("created")
        if datetime.now().day - 1 == message.created.day:
            return "Yesterday"
        elif datetime.today().date() == message.created.date():
            return message.created.strftime("%H:%M")
        else:
            return message.created.strftime("%d.%m.%y")

    def get_unread_messages(self, obj):
        return obj.messages.filter(readed=False).count()

    def get_current_user(self, obj):
        return self.user.username
