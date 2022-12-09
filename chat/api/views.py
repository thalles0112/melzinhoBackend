
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from rest_framework.viewsets import ModelViewSet

from chat.models import Chat, Message
from api.models import UserProfile
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def has(filtrar:list, arr:list):
    results = []
    for arg in filtrar:
        try:
            arr.index(arg)
        except:
            results.append(False)
        else:
            results.append(True)
    
    try:
        results.index(False)
    except:
        return True
    else:
        return False

User = get_user_model()



class ChatListView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    
    
    def get_queryset(self):
        tmparray = []
        queryset = []
        usernames = self.request.query_params.get('users', None)
        if usernames is not None:
            while len(queryset) == 0:
                
            
                for object in Chat.objects.all():
                    if has(usernames.split(','), str(object).split(',')[0:2]):
                        queryset = [object]
                        
                        break
                    else:
                        queryset =[]
                    
                if len(queryset) == 0:
                    usersArray = []
                    object = Chat.objects.create()
                    for user in usernames.split(','):
                        
                        object.participants.add(user)
                
                    object.save()
                    continue
                
                else:
                    break
        else:
            queryset = Chat.objects.all()
            
        return queryset
        
class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        
        queryset = []
        usernames = self.request.query_params.get('users', None)
        
            
        if usernames is not None:
            for object in Message.objects.all():
                if has(usernames.split(','), str(object).split(',')[0:2]):
                    queryset.append(object)
                    print(queryset)
                    
                
        
        return queryset

