#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import ListView

# Clase de la que heredaran otras para mostrar fotos en funcion de la autenticacion
class PhotosQuerySet(object):
    def get_photos_queryset(self, request):
        if not request.user.is_authenticated():
            # fotos publicas, no autenticado
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:
            # superuser
            photos = Photo.objects.all()
        else:
            # autenticado no admin, operacion a nivel de de bit con el |
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        return photos


# Ahora tenemos el controlador basado en clase
class HomeView(View):
    def get(self, request):
        """
        Convertimos nuestro home en una vista basada en clase
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

# Ahora tenemos el controlador basado en clase
class DetailView(View, PhotosQuerySet):
    def get(self, request, pk):
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
        # buscamos por clave primaria (pk), y también los elementos relacionados (en este caso el owner)
        # con .prefetch_related() obtendriamos la inversa: obteniendo un owner, traer sus fotos de golpe
        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner')

        # photo = (possible_photos.length ==1) ? possible_photos[0] : null; En teoría solo debería haber 1
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


class CreateView(View):
    # Decorador de Django que automáticamente me redirige a una url si no estoy autenticado
    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear una foto
        :param request: HttpRequest
        :return: HttpResponse
        """
        form = PhotoForm()
        context = {
            # Pasamos en el context los datos que se mostrarán en el template
            'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    # Decorador de Django que automáticamente me redirige a una url si no estoy autenticado
    @method_decorator(login_required())
    def post(self, request):
        """
        Crea una foto en base a la información POST
        :param request: HttpRequest
        :return: HttpResponse
        """
        success_message = ''
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user   # asigno como propietario de la foto el usuario autenticado
        form = PhotoForm(request.POST, instance=photo_with_owner)
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

class PhotoListView(View, PhotosQuerySet):
    def get(self, request):
        """
        Devuelve:
        - Las fotos publicas si el usuario no esta autenticado.
        - Las fotos del usuario autenticado o las publicas de todos.
        - Si el usuario es superadministrador, todas las fotos
        :param request:
        :return:
        """
        # ver queries avanzadas en documentacion de Django con el filter
        context = {
            # metodo estatico de la clase PhotosQuerySet
            'photos': self.get_photos_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)

class UserPhotosView(ListView):
    """
    Clase que hereda de las vistas genericas. Modelo es la foto y le indico la plantilla
    """
    model = Photo
    template_name = 'photos/user_photos.html'

    # Heredado de ListView, filtro del listado con el usuario que me llega del request
    def get_queryset(self):
        queryset = super(UserPhotosView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

