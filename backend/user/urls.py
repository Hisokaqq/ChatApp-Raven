from django.urls import path
from . import views

urlpatterns = [
        path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('register/', views.registerUser, name='register'),
        path('profile/', views.getUserProfile, name='user_info'),
        path('profile/<str:pk>', views.getSbProfile, name='user_info'),
        path('all/', views.getAllProfiles, name='all_users'),
        path('everybody/', views.get_everybody, name='all_users'),
        path('chatwith/', views.getChatUsers, name='chat_users'),
        path('friends/', views.getFriendsList, name='friends'),
        path('update/', views.updateUser, name='update'),
        path('follow/<str:pk>', views.friend_view, name='all_users'),
       
]