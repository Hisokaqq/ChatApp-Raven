from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    from_user_username = serializers.StringRelatedField(source='from_user.username')
    user_profile_avatar = serializers.ImageField(source='from_user.profile.avatar')
    class Meta:
        model = Message
        fields = "__all__"

    
    

class ConversationSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()
    
    last_message = serializers.SerializerMethodField()
    messages=MessageSerializer(many=True)
    class Meta:
        model = Conversation
        fields = "__all__"
    
    def get_last_message(self, conversation):
        last_message = conversation.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_user1(self, obj):
        return obj.users.all()[0].username if obj.get_users_count() == 2 else None

    def get_user2(self, obj):
        return obj.users.all()[1].username if obj.get_users_count() == 2 else None
    
