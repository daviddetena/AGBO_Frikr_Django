#-*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from photos.api import PhotoListAPI
from photos.views import HomeView, DetailView, CreateView, PhotoListView, UserPhotosView
from users.views import LoginView, LogoutView
from django.contrib.auth.decorators import  login_required
from users.api import UserListAPI, UserDetailAPI

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # PHOTO URLs
    # la primera parte es la url solicitada (Django construye el objeto HttpRequest) y lo pasa
    # a la función del controlador del segundo parametro
    # parametro name es para ponerle un nombre como referencia y no tener que harcodear la url
    # url(r'^$', 'photos.views.home', name='photos_home'),

    # Ahora la url esta basado en metodo de clase HomeView
    url(r'^$', HomeView.as_view(), name='photos_home'),

    # Fotos publicas si no esta autenticado, fotos propias de usuario registrado o publicas, si es
    # super admin, todas las fotos. Protejo contra no autorizados en my-photos
    url(r'^my-photos/$', login_required(UserPhotosView.as_view()), name='user_photos'),
    url(r'^photos/$', PhotoListView.as_view(), name='photos_list'),
    # pagina detalle foto, url empieza por /photos/id =>  ^ es inicio cadena, $ es fin cadena
    # ?P<pk> lo captura como parametro llamado 'pk'. [0-9]+ significa un numero 1 o mas veces
    url(r'^photos/(?P<pk>[0-9]+)$', DetailView.as_view(), name='photo_detail'),

    url(r'^photos/new$', CreateView.as_view(), name='create_photo'),

    # PHOTOS URLs
    url(r'^api/1.0/photos/$',PhotoListAPI.as_view(), name='photo_list_api'),


    # USERS URLs
    # Definimos login y logout basados en metodo de clase LoginView, LogoutView
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),


    # Users API URLs
    url(r'^api/1.0/users/$', UserListAPI.as_view(), name='user_list_api'),
    url(r'^api/1.0/users/(?P<pk>[0-9]+)$', UserDetailAPI.as_view(), name='user_detail_api'),
]
