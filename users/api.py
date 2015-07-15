#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from users.permissions import UserPermission


"""
Aquí ponemos todos los endpoints que el cliente REST solicitará.
En las clases de detalle donde implemento GET, PUT y DELETE a mano tengo que comprobar manualmente si el usuario puede
hacer lo que quiere hacer sobre el objeto indicado
"""

class UserListAPI(GenericAPIView):

    # Aplicamos nuestra propia clase de permisos
    permission_classes = (UserPermission,)

    """
    Heredamos ahora de GenericAPIView para que haga otras tareas inteligentes, como paginación o autenticación
    y autorización basada en clases
    """
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

    def post(self, request):
        """
        Creo nuevo usuario a partir de un objeto JSON
        :param request:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        # validamos serializador
        if serializer.is_valid():
            new_user = serializer.save()
            # debemos devolver un codigo 201 de creado nuevo objeto
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(GenericAPIView):
    """
    Heredamos ahora de GenericAPIView para que haga otras tareas inteligentes, como paginación o autenticación
    y autorización basada en clases
    """
    permission_classes = (UserPermission,)

    def get(self, request, pk):
        """
        Devolvemos la vista detalle de un usuario concreto. El filtro es que el pk sea el que me pasan
        :param request:
        :param pk: Parámetro con el pk del usuario
        :return: Si existe devuelve el objeto, si no devuelve un 404
        """
        user = get_object_or_404(User, pk=pk)
        #compruebo si el usuario autenticado puede hacer GET en este user, al recoger el objeto concreto manualmente
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Comprobamos si existe el usuario y actualizamos los datos. UserSerializer en este caso
        llamaría al método update del Serializer, ya que es el que recibe una instancia y también
        el validated_data
        :param request:
        :param pk: Parámetro con el pk del usuario
        :return: Si existe devuelve el objeto actualizado, si no devuelve un 404
        """
        # Obtenemos user
        user = get_object_or_404(User, pk=pk)
        #compruebo si el usuario autenticado puede hacer PUT en este user, al recoger el objeto concreto manualmente
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
         Comprobamos si existe el usuario y eliminamos los datos.
        :param request:
        :param pk:
        :return: Nada
        """
        user = get_object_or_404(User, pk=pk)
        #compruebo si el usuario autenticado puede hacer DELETE en este user, al recoger el objeto concreto manualmente
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
