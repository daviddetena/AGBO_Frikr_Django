#-*- coding: utf-8 -*-
from models import Photo
from photos.serializers import PhotoSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

"""
Heredamos de vistas genericas. Solo necesitamos indicarle el modelo del queryset y el serializer
para que automaticamente haga el metodo POST al api
"""
# get, post
class PhotoListAPI(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

# get, put, delete
class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

