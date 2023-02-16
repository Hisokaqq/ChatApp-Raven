from django.urls import path
from . import views

urlpatterns = [
    path("", views.getConversations , name="chats"),
    path('<str:pk>/message/create/', views.create_Message, name='create_message'),
    path("<str:pk>", views.getConversation , name="chat"),
    
    
]
print(32)