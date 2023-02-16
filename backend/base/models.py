from django.db import models

import uuid

from django.contrib.auth.models import User
from django.db import models



class Conversation(models.Model):
    users = models.ManyToManyField(to=User, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    def get_users_count(self):
        return self.users.count()

   
    

    def __str__(self):
        users_str = ", ".join([str(user) for user in self.users.all()])
        return f"({users_str})"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    content = models.CharField(max_length=10000)
    image = models.ImageField(null=True, blank=True, upload_to="message/")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}: {self.content} [{self.timestamp}]"