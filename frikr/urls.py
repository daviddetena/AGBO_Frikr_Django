#-*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # la primera parte es la url solicitada (Django construye el objeto HttpRequest) y lo pasa
    # a la función del controlador del segundo parametro
    url(r'^$', 'photos.views.home')
]
