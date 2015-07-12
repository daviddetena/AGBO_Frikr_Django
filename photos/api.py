#-*- coding: utf-8 -*-
from models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

"""
Heredamos de vistas genericas. Solo necesitamos indicarle el modelo del queryset y el serializer
para que automaticamente haga el metodo POST al api
"""
# get, post
class PhotoListAPI(ListCreateAPIView):
    queryset = Photo.objects.all()

    def get_serializer_class(self):
        """
        Sobreescribimos el atributo serializer_class para que devuelve la clase PhotoSerializer
        en el caso de una petición POST (crear nueva foto) o nuestra clase personalizada
        PhotoListSerializer solamente con los campos que nos interesan para el listado (id,name,url)
        :return:
        """
        return PhotoSerializer if self.request.method == "POST" else PhotoListSerializer


# get, put, delete
class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

