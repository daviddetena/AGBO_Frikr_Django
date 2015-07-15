#-*- coding: utf-8 -*-
from rest_framework import serializers
from models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo

class PhotoListSerializer(PhotoSerializer):
    """
    Esta clase hereda de la anterior, pero necesitamos que la clase Meta herede de la de Meta
    de PhotoSerializer, para que asigne Photo como model. Con esta función Meta indicamos
    los campos que queremos que nos devuelva la api del listado de fotos
    """
    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'name', 'url')