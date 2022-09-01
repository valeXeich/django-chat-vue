from django.contrib.auth.models import User

from rest_framework import viewsets, filters, generics
from rest_framework.response import Response

from .models import Chat
from .serializers import UserSerializer, ChatSerizlizer, ChatEnterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]

    def list(self, request, *args, **kwargs):
        chats = request.user.chat_set.all()
        qs = User.objects.exclude(chat__in=chats).exclude(username=request.user.username)
        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerizlizer

    def retrieve(self, request, *args, **kwargs):
        chat = self.get_object()
        for message in chat.messages.all():
            message.readed = True
            message.save()
        serializer = self.get_serializer(chat)
        companion = chat.participants.exclude(username=self.request.user.username)
        companion = companion.first().username
        return Response({"companion": companion, **serializer.data})


class ChatEnterListApiView(generics.ListAPIView):
    serializer_class = ChatEnterSerializer

    def get_queryset(self):
        if self.request.query_params.get("search", None):
            content = self.request.query_params["search"]
            users = User.objects.filter(username__icontains=content).exclude(
                username=self.request.user.username
            )
            search_result = Chat.objects.filter(participants__in=users).distinct()
            return search_result
        return self.request.user.chat_set.all()
