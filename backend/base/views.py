from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from django.contrib.auth.models import User
from rest_framework import status
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models import Q

@api_view(["GET"])
def getConversations(request):
    search = request.query_params.get("search")
    if search == None:
        search=""
    user = request.user
    conversations = Conversation.objects.filter(
        ~Q(users=user) | Q(users__username__icontains=search),
        messages__isnull=False
    ).annotate(last_message=Max('messages__timestamp')).order_by('-last_message')
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getConversation(request, pk):
    you = request.user
    user = User.objects.get(id=pk)
    chat = Conversation.objects.filter(users=user).filter(users=you)[0]
    
    serializer = ConversationSerializer(chat, many=False)
    
    return Response(serializer.data)

# @api_view(['POST'])
# def createMessage(request, conversation_id):
#     try:
#         conversation = Conversation.objects.get(id=conversation_id)
#     except Conversation.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     data = request.data.copy()
#     data['conversation'] = conversation.id
#     data['from_user'] = request.user.id

#     serializer = MessageSerializer(data=data)
#     if serializer.is_valid():
#         message = serializer.save()
#         return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_Message(request, pk):
    
    conversation = get_object_or_404(Conversation, pk=pk)
    
    user = request.user
    data = request.data
    # Find the other user in the conversation
    other_user = conversation.users.exclude(pk=user.pk).first()
    # Create a new message object
    message = Message.objects.create(
        conversation=conversation,
        from_user=user,
        to_user=other_user,
        content=data["text"]
    )
    
    # Serialize the message and return the response
    return Response({"details" : "message was created"}, status=status.HTTP_201_CREATED)