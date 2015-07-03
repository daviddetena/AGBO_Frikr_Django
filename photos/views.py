#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from photos.models import Photo, PUBLIC

def home(request):
    """
    Esta función devuelve el home de mi página. Quiero que me muestre todas las photos
    :param request: objeto HttpRequest
    :return: objeto HttpResponse con un html que contiene las fotos
    """
    # Recuperamos todos los objetos Photos (objects es objeto de clase ModelObject)
    # Aquí haría el SELECT * FROM photos, sin ejecutarlo
    photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
    context = {
        # Este es un parámetro de los que se pueden pasar al render, metidos en un diccionario
        #'photos_list': photos
        # me quedo con las 5 primeras
        # sólo aqui a ultima hora, cuando se utiliza, le añade al SELECT el LIMIT 5 y lo ejecuta
        'photos_list': photos[:5]
    }

    # Devolvemos la plantilla a traves del render
    return render(request, 'photos/home.html', context)