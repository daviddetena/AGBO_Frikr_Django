from django.db import models

# Globals
COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

LICENCES = (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative Commons')
)

# Clase que hereda del objeto Model para hacer ORM
class Photo(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)    # se guarda la primera vez que se crea
    modified_at = models.DateTimeField(auto_now=True)       # se actualiza cada vez que se guarde
    licence = models.CharField(max_length=3, choices=LICENCES)

    # Metodo especial de python, privado.
    # Hacemos que su representacion sea su nombre
    def __unicode__(self):
        return self.name
