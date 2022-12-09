from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import viewsets, status, generics, filters
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.dispatch import receiver
from django.shortcuts import render
from django.urls import reverse
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class AvisoViewset(viewsets.ModelViewSet):
    serializer_class = AvisoSerializer
    queryset = Aviso.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['-id']
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    

class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        userSerializer = UserSerializer(user, many=False)

        return Response({'token': token.key, 'user': userSerializer.data})

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(methods=['PUT'], detail=True, serializer_class=ChangePasswordSerializer)
    def change_pass(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'message':'Senha incorreta'},
    status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message':'Senha Alterada'}, status=status.HTTP_200_OK)


class ComentariosViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

class ComentariosList(generics.ListAPIView):
    serializer_class = ComentariosSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        aviso = self.request.query_params['aviso']
        return Comentario.objects.filter(aviso=aviso)

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)


class LikesList(generics.ListAPIView):
    serializer_class = LikesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        
        user = self.request.query_params['user']
        
        #self.request.query_params['aviso']
        try:
            aviso = self.request.query_params['aviso']
        except:
            queryset = Like.objects.filter(user=user)
        else:
            queryset = Like.objects.filter(user=user, aviso=aviso)
        return queryset


class OcupacaoViewSet(viewsets.ModelViewSet):
    serializer_class = OcupacaoSerializer
    queryset = Ocupacao.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

class SetorViewSet(viewsets.ModelViewSet):
    serializer_class = SetorSerializer
    queryset = Setor.objects.all()
# reset password function
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "https://melzinho.pythonanywhere.com/api/password-reset/confirm/?token={}".format(reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Redefinição de senha para Honeygram",
        # message:
        email_plaintext_message,
        # from:
        "honeygram.auth@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()



def password_reset_confirm(request, ):
    context = {'token': str(str(request).split('/')[-1]).replace('?token=', '').replace("'>", ''), 'csrftoken':RequestContext}
    return render(request, 'password_reset/reset.html', context)


