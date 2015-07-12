#-*- coding: utf-8 -*-
"""
    Aquí definimos los validadores para que sean comunes tanto a la validación del webform como
    a la del API
"""
from photos.settings import BADWORDS
from django.core.exceptions import ValidationError

def badwords_detector(value):
    """
    Valida si en 'value' se han puesto tacos definidos en settings.BADWORDS
    :return: Boolean
    """
    for badword in BADWORDS:
        if badword.lower() in value.lower():
            raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

    # Si va todo bien, devuelvo True
    return True