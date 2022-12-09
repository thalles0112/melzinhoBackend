from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'user_picture',
            'ocupacao',
            'return_user',
            'ocupacao',
            'setor'
            )

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password':{'write_only': True, 'required': False}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        Token.objects.create(user=user)
        return user

class AvisoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Aviso
        fields = (
            'id',
            'aviso_title',
            'add_separator',
            'content',
            'user',
            'return_user',
            'data',
            'media_content',
            'user_picture',
            'likes_counter'
            )



class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'id',
            'user',
            'aviso'
        )


class ComentariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields= (
            'id',
            'user',
            'aviso',
            'content',
            'time',
            'return_user',
            'user_picture'
        )

class OcupacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocupacao
        fields= (
                'id',
                'ocupacao_title'
            )

class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)