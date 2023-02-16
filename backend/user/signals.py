from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .serializers import ProfileSerializer
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
        )
           

post_save.connect(createProfile, sender=User)


# def deleteUser(sender, instance, **kwargs):
#     user = instance.user
#     user.delete()


# post_delete.connect(deleteUser, sender=Profile)
