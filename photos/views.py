#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from photos.models import Photo

def home(request):
    """
    Esta función devuelve el home de mi página. Quiero que me muestre todas las photos
    :param request: objeto HttpRequest
    :return: objeto HttpResponse con un html que contiene las fotos
    """
    # Recuperamos todos los objetos Photos (objects es objeto de clase ModelObject)
    photos = Photo.objects.all()

    html = '<ul>'
    for photo in photos:
        html += '<li>' + photo.name + '</li>'
    html += '</ul>'

    # Devolvemos en un HttpResponse el html creado
    return HttpResponse(html)