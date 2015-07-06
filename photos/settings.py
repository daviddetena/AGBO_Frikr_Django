#-*- coding: utf-8 -*-
# Importamos settings del proyecto
from django.conf import settings

# Globals
COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

DEFAULT_LICENCES = (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative Commons')
)

# Busca 'LICENCES' en los settings. Si no lo encuentra, el valor devuelto es DEFAULT_LICENCES
# Algo así como el .get de los elementos de diccionario
LICENCES = getattr(settings, 'LICENCES', DEFAULT_LICENCES)

# Si no hay nada en los settings generales, coge lista vacia de palabras inadecuadas
BADWORDS = getattr(settings, 'PROJECT_BADWORDS', [])