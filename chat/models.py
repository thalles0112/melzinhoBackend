from django.db import models
from django.contrib.auth import get_user_model
from api.models import UserProfile

User = get_user_model()





class Message(models.Model):
    author = models.ForeignKey(
        UserProfile, 
        related_name='message_author', 
        on_delete=models.CASCADE,
        unique=False)
    
    receiver = models.ForeignKey(
        UserProfile, 
        related_name='message_receiver', 
        on_delete=models.CASCADE,
        unique=False)

    sec_id = models.CharField(max_length=5000, unique=True, blank=True)
    
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.id},{self.receiver.id}'
        
        
        
        


class Chat(models.Model):
    participants = models.ManyToManyField(
        UserProfile, 
        related_name='chats', 
        blank=True)

    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        coolString = ''
        for participant in self.participants.all():
            coolString += str(participant.id)+','
        return coolString
        
        