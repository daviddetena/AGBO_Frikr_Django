#-*- coding: utf-8 -*-
from models import Photo
from photos.serializers import PhotoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class PhotoListAPI(APIView):

    def get(self, request):
        """
        Devolvemos todas las fotos
        :param request:
        :return:
        """
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)
