#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from photos.validators import badwords_detector
from photos.settings import LICENCES

PUBLIC = 'PUB'
PRIVATE = 'PRI'

VISIBILITY = (
    (PUBLIC, 'Pública'),
    (PRIVATE, 'Privada')
)


# Clase que hereda del objeto Model para hacer ORM
class Photo(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    url = models.URLField()
    # incluyo validador de description con la función indicada a nivel de modelo
    description = models.TextField(blank=True, null=True, default="", validators=[badwords_detector])
    created_at = models.DateTimeField(auto_now_add=True)    # se guarda la primera vez que se crea
    modified_at = models.DateTimeField(auto_now=True)       # se actualiza cada vez que se guarde
    licence = models.CharField(max_length=3, choices=LICENCES)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=PUBLIC)

    # Metodo especial de python, privado.
    # Hacemos que su representacion sea su nombre
    def __unicode__(self):
        return self.name
