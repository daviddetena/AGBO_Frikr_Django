#-*- coding: utf-8 -*-
__author__ = 'daviddetena'
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):

    # Definimos campos que queremos que se muestren cuando se envien/devuelven datos por http
    id = serializers.ReadOnlyField()      # id es de solo lectura
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crea una instancia User a partir de los datos de validated data, que contiene valores deserializados
        :param validated_data: Diccionario con datos de usuario
        :return: objeto User
        """
        # Creamos instancia y devolvemos la instancia de actualizar
        instance = User()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza instancia de User a partir de los datos del diccionario validated_data que contiene
        valores deserializados
        :param validated_data: Diccionario con datos de usuario
        :return: objeto User
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))

        # Guardamos en DB
        instance.save()
        return instance

    def validate_username(self, data):
        """
        Todos los metodos de validacion deben ser del tipo validate_<nombre_campo>
        Valida si existe un usuario con ese username
        :param data:
        :return:
        """
        users = User.objects.filter(username=data)
        if len(users) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        else:
            return data