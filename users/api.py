#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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
