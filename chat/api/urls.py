from django.urls import path, re_path
from django.conf.urls import include
from rest_framework import routers
from .views import (
    ChatListView,
    MessageViewSet,    
)

app_name = 'chat'

router = routers.DefaultRouter()


router.register(r'messages', MessageViewSet)




urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'chats', ChatListView.as_view()),
    
    
]

