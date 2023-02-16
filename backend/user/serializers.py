from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Friend

class FriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='friends.username')
    class Meta:
        model = Friend
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['checkMark', "avatar"]




from django.db.models import Subquery, OuterRef, Max
from base.models import Conversation, Message
from base.serializers import MessageSerializer


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    profile = ProfileSerializer()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "isAdmin", "first_name", "last_name", "date_joined", "profile", "last_message", "user",]
    
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_last_message(self, obj):
        conversation = Conversation.objects.filter(users=obj.id)
        latest_message = conversation.filter(messages__isnull=False).annotate(last_message=Max('messages__timestamp')).values('last_message').order_by('-last_message').first()

        if latest_message:
            latest_message = Message.objects.filter(conversation__in=conversation, timestamp=latest_message['last_message']).first()
            return MessageSerializer(latest_message).data
        return None



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "isAdmin", "token", "first_name", "last_name" ,"date_joined", "profile",  "last_message",  "user"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

