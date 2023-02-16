from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserSerializerWithToken, FriendSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Friend
from rest_framework import status
from django.db.models import Q
from base.models import Conversation, Message
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def getSbProfile(request, pk):
    you = request.user
    user = User.objects.get(id=pk)
    chat = Conversation.objects.filter(users=user).filter(users=you)
    
    if not chat.exists():
        chat = Conversation.objects.create()
        chat.users.add(you, user)
        chat.save()
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

from django.db.models import Exists, OuterRef, Subquery

@api_view(["GET"])
def getAllProfiles(request):
    search = request.query_params.get("search")
    if search == None:
        search=""
    if(len(search)==0):
        users = []
        serializer = UserSerializerWithToken(users, many=True)
        return Response(serializer.data)
    user = request.user
    # get a list of user ids who have sent or received messages to/from the authorized user
    user_ids_with_messages = Message.objects.filter(Q(from_user=user) | Q(to_user=user)).values_list('from_user', 'to_user')
    # get a list of user ids to exclude from the queryset
    exclude_user_ids = set(sum(user_ids_with_messages, ()))  # merge the list of user ids and convert to a set to remove duplicates
    # get a queryset of users excluding the authorized user and the users with messages in conversation with the authorized user
    users = User.objects.exclude(Q(id=user.id) | Q(id__in=exclude_user_ids)).filter(username__icontains=search)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


from django.db.models import Max

@api_view(["GET"])
def getChatUsers(request):
    search = request.query_params.get("search")
    if search == None:
        search = ""
    user = request.user
    user_ids_with_messages = Message.objects.filter(Q(from_user=user) | Q(to_user=user)).values_list('from_user', 'to_user')
    include_user_ids = set(sum(user_ids_with_messages, ()))  # merge the list of user ids and convert to a set to remove duplicates
    users = User.objects.filter(id__in=include_user_ids).exclude(id=user.id).filter(username__icontains=search)
    users = users.annotate(last_message=Max('conversation__messages__timestamp')).order_by('-last_message')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_everybody(request):
    users = User.objects.all()
    users = User.objects.order_by('-username')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFriendsList(request):
    user = request.user
    users = User.objects.filter(~Q(id=user.id))
    friends = Friend.objects.filter(user=user)
    friends_ids = [value.friends.id for value in friends]
    users = users.filter(
        id__in=[value for value in friends_ids]
    )

    serializer = UserSerializerWithToken(users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            username = data["username"],
            email = data["email"],
            password = make_password(data["password"])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "user with this username already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
 



@api_view(['POST'])
def friend_view(request, pk):
    user = request.user
    try:
        to_follow = User.objects.get(id=pk)
        are_friends = Friend.objects.filter(user=user, friends=to_follow)
        if are_friends:
            are_friends.delete()
            message = {"detail": "no friends anymore"}
        else:
            friendship = Friend.objects.create(
                user=user, 
                friends=to_follow
            )
            friendship.save()
            message = {"detail": "added"}
            you = request.user
            user = User.objects.get(id=pk)
            chat = Conversation.objects.filter(users=user).filter(users=you)
            
            if not chat.exists():
                chat = Conversation.objects.create()
                chat.users.add(you, user)
                chat.save()
            
    except:
        message = {"detail": "No such a user"}
    return Response(message)

@api_view(["PUT", "GET"])
def updateUser(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many = False)
    data = request.data
    
    return Response(serializer.data)

