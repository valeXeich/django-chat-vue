from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Sender: {self.sender}, text: {self.text}"


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=200, blank=True)
    group = models.BooleanField(default=False)
    messages = models.ManyToManyField(Message, blank=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.participants.all()[0]} - {self.participants.all()[1]}"
