#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class UserListAPI(APIView):

    def get(self, request):
        """
        Queremos devolver todos los usuarios del sistema
        :param request:
        :return:
        """
        users = User.objects.all()
        # voy a serializar todos los objetos que le pase
        serializer = UserSerializer(users, many=True)
        serialized_users = serializer.data
        return Response(serialized_users)


class UserDetailAPI(APIView):

    def get(self, request, pk):
        """
        Devolvemos la vista detalle de un usuario concreto. El filtro es que el pk sea el que me pasan
        :param request:
        :param pk: Parámetro con el pk del usuario
        :return: Si existe devuelve el objeto, si no devuelve un 404
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)