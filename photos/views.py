#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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


# Decorador de Django que automáticamente me redirige a una url si no estoy autenticado
@login_required()
def create(request):
    """
    Muestra un formulario para crear una foto y la crea si la petición es POST
    :param request: HttpRequest
    :return: HttpResponse
    """
    success_message = ''
    if request.method == 'GET':
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST)
        if form.is_valid():
            # Guarda el objeto del formulario en la DB y lo devuelve
            new_photo = form.save()

            # Inicializamos formulario, con el reverse componemos la url dinámica que mostrará con la nueva
            # foto
            form = PhotoForm()
            success_message = 'Guardado con éxito!'
            success_message += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
    context = {
        # Pasamos en el context los datos que se mostrarán en el template
        'form': form,
        'success_message': success_message
    }
    return render(request, 'photos/new_photo.html', context)
