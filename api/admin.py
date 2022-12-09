from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'user_picture', 'ocupacao', 'setor')
    list_display = ('user', 'ocupacao', 'setor')


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    fields = ('aviso_title', 'content', 'media_content', 'user')
    list_display = ('id','aviso_title', 'content', 'likes_counter', 'data')


@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    fields = ('user', 'aviso')
    list_display = ('user', 'aviso')


@admin.register(Comentario)
class CommentAdmin(admin.ModelAdmin):
    fields = ('user', 'aviso', 'data', 'content')
    list_display = ('user', 'aviso', 'data')

@admin.register(Ocupacao)
class OcupacaoAdmin(admin.ModelAdmin):
    fields = ('ocupacao_title', 'ocupacao_picture')
    list_display = ('ocupacao_title', 'ocupacao_picture')

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    fields = ('setor_title', 'setor_picture', 'ocupacoes')
    list_display = ('setor_title', 'setor_picture')
