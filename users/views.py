#-*- coding: utf-8 -*-
# Controlador para funciones de usuario
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate


def login(request):
    """
    Comprobamos usuario
    :param request:
    :return:
    """
    error_messages = []
    if request.method == 'POST':
        # En Python NO acceder nunca mediante corchete a la clave de un diccionario
        # Si usamos el .get(,) nos comprueba que exista la clave, o devuelve lo del 2º param
        username = request.POST.get('usr')
        password = request.POST.get('pwd')

        # Encripta la contraseña automaticamente para comprobar sus credenciales. Si no existe
        # usuario, devuelve nulo
        user = authenticate(username=username, password=password)
        if user is None:
            error_messages.append('Nombre de usuario o contraseña incorrectos')
        else:
            if user.is_active:
                # Activamos sesion
                django_login(request, user)
                return redirect('photos_home')
            else:
                error_messages.append('El usuario no está activo')
    context = {
        'errors': error_messages
    }
    # Hacemos que el render tenga disponible el contexto con los datos que pasamos de error
    return render(request, 'users/login.html', context)

def logout(request):
    # Desautenticamos usuario y redirigimos al home
    if request.user.is_authenticated():
        # django tiene su propia funcion logout
        django_logout(request)
    return redirect('photos_home')
