#-*- coding: utf-8 -*-
from models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from photos.views import PhotosQuerySet

# TO-DO: implementar una nueva clase con la información que comparten PhotoListAPI y PhotoDetailAPI
# y hacer que estas dos hereden de la nueva, la cual heredará de PhotosQuerySet


"""
Heredamos de vistas genericas. Solo necesitamos indicarle el modelo del queryset y el serializer
para que automaticamente haga el metodo POST al api. Heredamos tambíen de photos.view para generar
las autorizaciones utilizando el método get_photos_queryset ya definido
"""
# get, post
class PhotoListAPI(PhotosQuerySet, ListCreateAPIView):
    queryset = Photo.objects.all()
    # Permisos de lectura para todos y de añadir/escribir/eliminar sólo para autenticados
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """
        Sobreescribimos el atributo serializer_class para que devuelve la clase PhotoSerializer
        en el caso de una petición POST (crear nueva foto) o nuestra clase personalizada
        PhotoListSerializer solamente con los campos que nos interesan para el listado (id,name,url)
        :return:
        """
        return PhotoSerializer if self.request.method == "POST" else PhotoListSerializer

    def get_queryset(self):
        """
        Heredamos el método de photos.views.py para asignar las autorizaciones dinámicamente que contiene dicha clase
        :return:
        """
        return self.get_photos_queryset(self.request)

    # Sobreescribimos perform_create para que al llamar a serializer.save(), coja el usuario autenticado como el
    # propietario de la nueva foto
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# get, put, delete
class PhotoDetailAPI(PhotosQuerySet, RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # Permisos de lectura para todos y de añadir/escribir/eliminar sólo para autenticados
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Heredamos el método de photos.views.py para asignar las autorizaciones dinámicamente
        :return:
        """
        return self.get_photos_queryset(self.request)

