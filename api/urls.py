from api import views
from rest_framework import routers
from django.urls import re_path
from django.conf.urls import include





router = routers.DefaultRouter()
router.register(r'avisos', views.AvisoViewset)
router.register(r'userprofile', views.UserProfileViewset)
router.register(r'users', views.UsersViewSet)
router.register(r'likes', views.LikesViewSet)
router.register(r'comentarios', views.ComentariosViewSet)
router.register(r'ocupacoes', views.OcupacaoViewSet)
router.register(r'setor', views.SetorViewSet)



urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path('auth/', views.CustomObtainAuthToken.as_view()),
    re_path(r'password-reset/confirm/', views.password_reset_confirm),
    re_path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path(r'comentarios_post/', views.ComentariosList.as_view()),
    re_path(r'likes_user', views.LikesList.as_view()),


]