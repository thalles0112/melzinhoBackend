
import django
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
# reset password configs





class Ocupacao(models.Model):
    ocupacao_title = models.CharField(max_length=64, blank=True)
    ocupacao_picture = models.CharField(max_length=256, blank=True)
    def __str__(self):
        return str(self.ocupacao_title)

class Setor(models.Model):
    setor_title = models.CharField(max_length=64, blank=True)
    setor_picture = models.CharField(max_length=256, blank=True)
    ocupacoes = models.ManyToManyField(Ocupacao)

    def __str__(self):
        return str(self.setor_title)
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    user_picture = models.CharField(max_length=256, blank=True)
    ocupacao = models.ForeignKey(Ocupacao, related_name='ocupacao', on_delete=models.CASCADE, blank=True)
    setor = models.ForeignKey(Setor, related_name='setor', on_delete=models.CASCADE, blank=True)

    def return_user(self):
        return str(self.user)

    def __str__(self):
        return str(self.user)

class Aviso(models.Model):
    aviso_title = models.CharField(max_length=128, null=True, unique=False, blank=True)
    media_content = models.CharField(max_length=256, blank=True)
    content = models.TextField(max_length=256, null=False, unique=False, blank=True)
    data = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile')
    likes = models.ManyToManyField(User, through='api.Like')

    def add_separator(self):
        return self.aviso_title.__str__().replace(' ', '-')

    def likes_counter(self):
        likes = 0
        for u in Like.objects.all():

            if u.aviso_id == self.id:
                likes += 1
        return likes

    def comentarios_counter(self):
        comments = 0
        for u in Comentario.objects.all():

            if u.aviso_id == self.id:
                comments += 1
        return comments

    def return_user(self):
        return str(self.user)

    def __str__(self):
        return str(self.aviso_title)

    def user_picture(self):
        for p in UserProfile.objects.all():
            if str(p.user) == str(self.user):
                return p.user_picture




class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aviso = models.ForeignKey(Aviso, on_delete=models.CASCADE)
    class Meta:
        unique_together = [('aviso', 'user')]


class Comentario(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    aviso = models.ForeignKey(Aviso, models.CASCADE)
    content = models.TextField(max_length=256, null=False, unique=False)
    data = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    def return_user(self):
        return str(self.user)

    def user_picture(self):
        for p in UserProfile.objects.all():
            if str(p.user) == str(self.user):
                return p.user_picture


