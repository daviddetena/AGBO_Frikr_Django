#-*- coding: utf-8 -*-
from rest_framework import serializers
from models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        # POST
        # Indicamos que el campo owner será de sólo lectura, para que no sea obligatorio incluirlo
        # para crear una nueva foto (ya que cogerá el usuario autenticado definido en la api), pero
        # sí para que me aparezca como respuesta. tupla read_only_fields(). Funciona para post (esta
        # clase), y para put, get, delete (PhotoListSerializer que hereda de esta)
        read_only_fields = ('owner',)

class PhotoListSerializer(PhotoSerializer):
    """
    Esta clase hereda de la anterior, pero necesitamos que la clase Meta herede de la de Meta
    de PhotoSerializer, para que asigne Photo como model. Con esta función Meta indicamos
    los campos que queremos que nos devuelva la api del listado de fotos
    """
    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'name', 'url')