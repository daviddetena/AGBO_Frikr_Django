#-*- coding: utf-8 -*-
# Controlador para funciones de usuario
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from users.forms import LoginForm

def login(request):
    """
    Comprobamos usuario
    :param request:
    :return:
    """

    error_messages = []
    if request.method == 'POST':
        # Recoge todos los datos del post y los limpia
        form = LoginForm(request.POST)

        # Validamos formulario
        if form.is_valid():
            # En Python NO acceder nunca mediante corchete a la clave de un diccionario
            # form.cleaned_data contendrá los datos limpiados de los campos que recojamos (que están en el /users/forms.py)

            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')

            # Encripta la contraseña automaticamente para comprobar sus credenciales. Si no existe
            # usuario, devuelve nulo
            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrectos')
            else:
                if user.is_active:
                    # Activamos sesion
                    django_login(request, user)
                    # next contiene la siguiente pagina a la que navegar. Si no existe, lo manda a photos_home
                    url = request.GET.get('next', 'photos_home')
                    return redirect(url)
                else:
                    error_messages.append('El usuario no está activo')
    else:
        # Por GET el formulario no existe
        form = LoginForm()
    context = {
        'errors': error_messages,
        'login_form': form
    }
    # Hacemos que el render tenga disponible el contexto con los datos que pasamos de error
    return render(request, 'users/login.html', context)

def logout(request):
    # Desautenticamos usuario y redirigimos al home
    if request.user.is_authenticated():
        # django tiene su propia funcion logout
        django_logout(request)
    return redirect('photos_home')
