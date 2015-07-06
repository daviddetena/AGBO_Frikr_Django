#-*- coding: utf-8 -*-
__author__ = 'daviddetena'

from django import forms
from photos.models import Photo
from photos.settings import BADWORDS
from django.core.exceptions import ValidationError

class PhotoForm(forms.ModelForm):
    """
    Formulario para el modelo Photo
    """
    # Meta clase para el modelo photo
    class Meta:
        model = Photo
        exclude = ['owner']

    def clean(self):
        """
        Valida si en la descripción se han puesto tacos definidos en settings.BADWORDS
        :return: diccionario con los atributos si OK
        """
        cleaned_data = super(PhotoForm,self).clean()

        # Recupero description del diccionario del formulario
        description = cleaned_data.get('description', '')

        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise ValidationError(u'La palabra {0} no está permitida',format(badword))

        # Si va todo bien, devuelvo los datos limpios/normalizados
        return cleaned_data