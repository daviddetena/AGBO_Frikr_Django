#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):
    """
    En esta clase definiremos nuestra propia política de permisos de usuario:
    - Un superusuario podrá ver/añadir/modificar/eliminar cualquiera
    - Un usuario no autenticado sólo podrá añadir una cuenta
    - Un usuario autenticado sólo podrá realizar operaciones de modificación o eliminación sobre su propia cuenta de
    usuario. No podrá hacer un GET con el listado de usuarios, pero sí de su cuenta (vista detalle)
    """
    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción (GET,POST,PUT o DELETE)
        :param request:
        :param view:
        :return:
        """
        from users.api import UserDetailAPI     # Carga perezosa para evitar dependencia ciclica

        # cualquier usuario puede crear su propia cuenta
        if request.method == "POST":
            return True
        # si no es POST, super usuario siempre puede
        elif request.user.is_superuser:
            return True
        # si es GET a vista de detalle de usuario, tomo la decisión en has_object_permissions
        elif isinstance(view, UserDetailAPI):
            return True
        else:
            # Prohibido el GET a /api/1.0/users/
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción (GET,POST,PUT o DELETE)
        sobre el objeto obj, es decir, para vistas de detalle
        :param request:
        :param view:
        :param obj:
        :return:
        """
        # Si es superadmin, o el usuario autenticado intenta
        # hacer GET, PUT o DELETE sobre su mismo perfil, lo permitimos
        return request.user.is_superuser or request.user == obj
