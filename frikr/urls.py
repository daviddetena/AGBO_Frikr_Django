#-*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # PHOTO URLs
    # la primera parte es la url solicitada (Django construye el objeto HttpRequest) y lo pasa
    # a la función del controlador del segundo parametro
    # parametro name es para ponerle un nombre como referencia y no tener que harcodear la url
    url(r'^$', 'photos.views.home', name='photos_home'),

    # pagina detalle foto, url empieza por /photos/id =>  ^ es inicio cadena, $ es fin cadena
    # ?P<pk> lo captura como parametro llamado 'pk'. [0-9]+ significa un numero 1 o mas veces
    url(r'^photos/(?P<pk>[0-9]+)$', 'photos.views.detail', name='photo_detail'),
    url(r'^photos/new$', 'photos.views.create', name='create_photo'),

    # USERS URLs
    url(r'^login$', 'users.views.login', name='users_login'),
    url(r'^logout$', 'users.views.logout', name='users_logout')
]
