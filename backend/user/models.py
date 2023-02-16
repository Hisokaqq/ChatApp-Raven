from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="profiles/")
    checkMark = models.BooleanField(null=True, blank=True, default=False)
    def __str__(self):
        return str(self.user)



class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    def __str__(self):
        return f"{str(self.user)} + {str(self.friends)}"

