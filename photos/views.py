#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound
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


def detail(request, pk):
    """
    Carga la pagina de detalle de foto
    :param request: HttpRequest
    :param pk: PRIMARY KEY de la foto
    :return: HttpResponse
    """
    """
    try:
        photo = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        photo = None
    except Photo.MultipleObjects:
        photo = None
    """
    # buscamos por clave primaria (pk)
    possible_photos = Photo.objects.filter(pk=pk)

    # photo = (possible_photos.length ==1) ? posible_photos[0] : null;
    photo = possible_photos[0] if len(possible_photos) >= 1 else None

    if photo is not None:
        # cargar plantilla de detalle. Parámetro photo es lo que se recogerá en la vista
        context = {
            'photo': photo
        }
        return render(request, 'photos/detail.html', context)
    else:
        # 404 not found
        return HttpResponseNotFound("No existe la foto")
